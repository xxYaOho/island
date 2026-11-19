from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ledger.alpha import read_alpha


class AlphaParserTest(unittest.TestCase):
    def test_parses_signed_minor_units_and_normalizes_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            csv_path = Path(temporary) / "alpha.csv"
            csv_path.write_text(
                "交易时间,交易单号,交易对象,类型,金额,分类\n"
                "2026-09-01T09:00:00+08:00,A-9,  Acme   Corp  ,收入,8000.00,收入\n",
                encoding="utf-8",
            )
            transaction = read_alpha(csv_path, "main")[0]

        self.assertEqual(transaction["amount_minor"], 800000)
        self.assertEqual(transaction["target"], "Acme Corp")
        self.assertEqual(transaction["source"]["row"], 2)


if __name__ == "__main__":
    unittest.main()
