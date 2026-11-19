from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data" / "ledger.json"


class LedgerCliTest(unittest.TestCase):
    def test_list_returns_seed_transaction(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "ledger.cli", "list", "--ledger", str(SEED)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["transactions"][0]["transaction_id"], "A-1001")

    def test_import_alpha_adds_once_then_skips_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp_root = Path(temporary)
            ledger_path = temp_root / "ledger.json"
            csv_path = temp_root / "alpha.csv"
            shutil.copyfile(SEED, ledger_path)
            csv_path.write_text(
                "交易时间,交易单号,交易对象,类型,金额,分类\n"
                "2026-09-01T09:00:00+08:00,A-1002,Acme Corp,收入,8000.00,收入\n",
                encoding="utf-8",
            )

            first = self._import(ledger_path, csv_path)
            second = self._import(ledger_path, csv_path)

        self.assertEqual(first, {"added": 1, "duplicates": 0})
        self.assertEqual(second, {"added": 0, "duplicates": 1})

    def _import(self, ledger_path: Path, csv_path: Path) -> dict[str, int]:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "ledger.cli",
                "import-alpha",
                "--ledger",
                str(ledger_path),
                "--account",
                "alpha-main",
                "--file",
                str(csv_path),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)


if __name__ == "__main__":
    unittest.main()
