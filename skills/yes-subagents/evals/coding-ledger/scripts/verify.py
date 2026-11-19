#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = PACKAGE_ROOT / "fixture" / "inputs"
SEED_LEDGER = PACKAGE_ROOT / "fixture" / "ledger-cli" / "data" / "ledger.json"
EXPECTED = json.loads((PACKAGE_ROOT / "oracle" / "expected.json").read_text(encoding="utf-8"))


class Verification:
    def __init__(self, case: str) -> None:
        self.case = case
        self.checks: list[dict[str, object]] = []

    def add(self, name: str, passed: bool, evidence: str) -> None:
        self.checks.append({"name": name, "passed": passed, "evidence": evidence})

    @property
    def passed(self) -> bool:
        return all(bool(item["passed"]) for item in self.checks)


def run_cli(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "ledger.cli", *args],
        cwd=repo,
        env=environment,
        capture_output=True,
        text=True,
    )


def parse_json_output(completed: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise ValueError("command produced no stdout")
    payload = json.loads(lines[-1])
    if not isinstance(payload, dict):
        raise ValueError("last stdout line is not a JSON object")
    return payload


def compare_counts(
    verification: Verification,
    name: str,
    completed: subprocess.CompletedProcess[str],
    expected: dict[str, int],
) -> dict[str, Any] | None:
    if completed.returncode != 0:
        verification.add(name, False, f"exit={completed.returncode}; stderr={completed.stderr.strip()}")
        return None
    try:
        payload = parse_json_output(completed)
    except Exception as error:
        verification.add(name, False, str(error))
        return None
    actual = {key: payload.get(key) for key in expected}
    verification.add(name, actual == expected, f"actual={actual!r}; expected={expected!r}")
    return payload


def transaction_map(ledger_path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(ledger_path.read_text(encoding="utf-8"))
    result: dict[str, dict[str, Any]] = {}
    for transaction in payload["transactions"]:
        key = "|".join(
            [transaction["bank"], transaction["account"], transaction["transaction_id"]]
        )
        result[key] = transaction
    return result


def verify_transactions(verification: Verification, ledger_path: Path) -> None:
    expected = EXPECTED["thick_m1"]
    actual = transaction_map(ledger_path)
    verification.add(
        "transaction-count",
        len(actual) == expected["transaction_count"],
        f"actual={len(actual)}; expected={expected['transaction_count']}",
    )
    verification.add(
        "transaction-keys",
        set(actual) == set(expected["transactions"]),
        f"missing={sorted(set(expected['transactions']) - set(actual))}; extra={sorted(set(actual) - set(expected['transactions']))}",
    )
    for key, wanted in expected["transactions"].items():
        if key not in actual:
            continue
        transaction = actual[key]
        source = transaction.get("source", {})
        projected = {
            "occurred_at": transaction.get("occurred_at"),
            "amount_minor": transaction.get("amount_minor"),
            "currency": transaction.get("currency"),
            "kind": transaction.get("kind"),
            "target": transaction.get("target"),
            "category": transaction.get("category"),
            "source_file": source.get("file"),
            "source_row": source.get("row"),
        }
        verification.add(f"transaction:{key}", projected == wanted, f"actual={projected!r}")
        verification.add(
            f"source-raw:{key}",
            isinstance(source.get("raw"), dict) and bool(source["raw"]),
            f"raw_type={type(source.get('raw')).__name__}",
        )


def populate_thick(verification: Verification, repo: Path, ledger_path: Path) -> bool:
    expected = EXPECTED["thick_m1"]["imports"]
    commands = [
        (
            "alpha-primary",
            expected["alpha_primary"],
            (
                "import-csv", "--ledger", str(ledger_path), "--bank", "alpha",
                "--account", "alpha-main", "--file", str(INPUT_ROOT / "thick-alpha.csv"),
            ),
        ),
        (
            "beta-primary",
            expected["beta_primary"],
            (
                "import-csv", "--ledger", str(ledger_path), "--bank", "beta",
                "--account", "beta-card", "--file", str(INPUT_ROOT / "thick-beta.csv"),
            ),
        ),
        (
            "alpha-repeat",
            expected["alpha_repeat"],
            (
                "import-csv", "--ledger", str(ledger_path), "--bank", "alpha",
                "--account", "alpha-main", "--file", str(INPUT_ROOT / "thick-alpha.csv"),
            ),
        ),
        (
            "alpha-conflict",
            expected["alpha_conflict"],
            (
                "import-csv", "--ledger", str(ledger_path), "--bank", "alpha",
                "--account", "alpha-main", "--file", str(INPUT_ROOT / "thick-alpha-conflict.csv"),
            ),
        ),
    ]
    for name, wanted, args in commands:
        completed = run_cli(repo, *args)
        if compare_counts(verification, name, completed, wanted) is None:
            return False

    before_bad_header = ledger_path.read_bytes()
    bad_header = run_cli(
        repo,
        "import-csv", "--ledger", str(ledger_path), "--bank", "alpha",
        "--account", "alpha-main", "--file", str(INPUT_ROOT / "thick-alpha-bad-header.csv"),
    )
    verification.add(
        "file-level-failure",
        bad_header.returncode != 0 and ledger_path.read_bytes() == before_bad_header,
        f"exit={bad_header.returncode}; unchanged={ledger_path.read_bytes() == before_bad_header}",
    )

    before_legacy = ledger_path.read_bytes()
    legacy = run_cli(
        repo,
        "import-alpha", "--ledger", str(ledger_path), "--account", "alpha-main",
        "--file", str(INPUT_ROOT / "thin-alpha.csv"),
    )
    verification.add(
        "legacy-import-alpha",
        legacy.returncode == 0 and ledger_path.read_bytes() == before_legacy,
        f"exit={legacy.returncode}; unchanged={ledger_path.read_bytes() == before_legacy}",
    )
    return True


def verify_thin(verification: Verification, repo: Path, ledger_path: Path) -> None:
    before = ledger_path.read_bytes()
    completed = run_cli(
        repo,
        "import-alpha", "--ledger", str(ledger_path), "--account", "alpha-main",
        "--file", str(INPUT_ROOT / "thin-alpha.csv"), "--dry-run",
    )
    compare_counts(verification, "dry-run-summary", completed, EXPECTED["thin"]["summary"])
    after = ledger_path.read_bytes()
    verification.add("ledger-byte-stability", before == after, f"unchanged={before == after}")
    count = len(transaction_map(ledger_path))
    verification.add(
        "ledger-transaction-count",
        count == EXPECTED["thin"]["transaction_count"],
        f"actual={count}; expected={EXPECTED['thin']['transaction_count']}",
    )


def normalize_rows(payload: dict[str, Any]) -> dict[str, dict[str, int]]:
    rows = payload.get("rows")
    if isinstance(rows, dict):
        return rows
    if not isinstance(rows, list):
        raise ValueError("report rows must be an object or array")
    result: dict[str, dict[str, int]] = {}
    for row in rows:
        group = row["group"]
        result[group] = {
            "transaction_count": row["transaction_count"],
            "cashflow_minor": row["cashflow_minor"],
            "spend_minor": row["spend_minor"],
        }
    return result


def verify_report(
    verification: Verification,
    repo: Path,
    ledger_path: Path,
    name: str,
    period: str,
    anchor: str,
    group_by: str,
) -> None:
    args = (
        "report", "--ledger", str(ledger_path), "--period", period,
        "--anchor", anchor, "--group-by", group_by, "--format", "json",
    )
    first = run_cli(repo, *args)
    second = run_cli(repo, *args)
    if first.returncode != 0 or second.returncode != 0:
        verification.add(name, False, f"exit={first.returncode}/{second.returncode}; stderr={first.stderr.strip()}")
        return
    try:
        payload = parse_json_output(first)
        wanted = EXPECTED["thick_m2"]["reports"][name]
        actual = {
            "period_start": payload.get("period_start"),
            "period_end": payload.get("period_end"),
            "rows": normalize_rows(payload),
        }
    except Exception as error:
        verification.add(name, False, str(error))
        return
    verification.add(name, actual == wanted, f"actual={actual!r}")
    verification.add(
        f"{name}-stable-output",
        first.stdout == second.stdout,
        f"identical={first.stdout == second.stdout}",
    )


def verify_thick_m2(verification: Verification, repo: Path, ledger_path: Path) -> None:
    cases = [
        ("week_category", "week", "2026-09-03", "category"),
        ("week_target", "week", "2026-09-03", "target"),
        ("month_category", "month", "2026-09-15", "category"),
        ("month_target", "month", "2026-09-15", "target"),
    ]
    for case in cases:
        verify_report(verification, repo, ledger_path, *case)

    table = run_cli(
        repo,
        "report", "--ledger", str(ledger_path), "--period", "week",
        "--anchor", "2026-09-03", "--group-by", "category",
    )
    stripped = table.stdout.lstrip()
    is_table = table.returncode == 0 and bool(stripped) and stripped[0] not in "[{"
    verification.add("default-table-output", is_table, f"exit={table.returncode}; stdout={table.stdout[:120]!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Black-box verification for coding-ledger eval")
    parser.add_argument("--case", required=True, choices=("thin", "thick-m1", "thick-m2"))
    parser.add_argument("repo", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    verification = Verification(args.case)

    if not (repo / "ledger" / "cli.py").is_file():
        verification.add("repo-shape", False, f"missing ledger/cli.py under {repo}")
    else:
        with tempfile.TemporaryDirectory(prefix="coding-ledger-verify-") as temporary:
            ledger_path = Path(temporary) / "ledger.json"
            shutil.copyfile(SEED_LEDGER, ledger_path)
            if args.case == "thin":
                verify_thin(verification, repo, ledger_path)
            else:
                populated = populate_thick(verification, repo, ledger_path)
                if populated:
                    verify_transactions(verification, ledger_path)
                    if args.case == "thick-m2":
                        verify_thick_m2(verification, repo, ledger_path)

    result = {
        "case": args.case,
        "status": "PASS" if verification.passed else "FAIL",
        "checks": verification.checks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if verification.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
