#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "manifest.json",
    "host/TRUTH_CARD.md",
    "host/RUBRIC.md",
    "host/dispatch-contract.md",
    "host/observation-schema.json",
    "host/REPORT_TEMPLATE.md",
    "cases/thin/Decision.md",
    "cases/thin/Draft.md",
    "cases/thin/PROMPT_STEP_1.md",
    "cases/thin/PROMPT_STEP_2.md",
    "cases/thick/Decision.md",
    "cases/thick/Draft.md",
    "cases/thick/PROMPT_STEP_1.md",
    "cases/thick/PROMPT_STEP_2.md",
    "fixture/ledger-cli/ledger/cli.py",
    "fixture/ledger-cli/data/ledger.json",
    "fixture/inputs/thin-alpha.csv",
    "fixture/inputs/thick-alpha.csv",
    "fixture/inputs/thick-beta.csv",
    "fixture/inputs/thick-alpha-conflict.csv",
    "fixture/inputs/thick-alpha-bad-header.csv",
    "oracle/expected.json",
    "scripts/prepare.py",
    "scripts/check_oracle.py",
    "scripts/verify.py",
]

PROMPTS = [
    "cases/thin/PROMPT_STEP_1.md",
    "cases/thin/PROMPT_STEP_2.md",
    "cases/thick/PROMPT_STEP_1.md",
    "cases/thick/PROMPT_STEP_2.md",
]

VISIBLE_UPSTREAM = [
    "cases/thin/Decision.md",
    "cases/thin/Draft.md",
    "cases/thick/Decision.md",
    "cases/thick/Draft.md",
]


class Checks:
    def __init__(self) -> None:
        self.results: list[dict[str, object]] = []

    def add(self, name: str, passed: bool, detail: str) -> None:
        self.results.append({"name": name, "passed": passed, "detail": detail})

    @property
    def passed(self) -> bool:
        return all(bool(item["passed"]) for item in self.results)


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def csv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def main() -> int:
    checks = Checks()

    missing = [name for name in REQUIRED_FILES if not (PACKAGE_ROOT / name).is_file()]
    checks.add("required-files", not missing, "missing=" + repr(missing))

    parsed_json: dict[str, object] = {}
    for name in ("manifest.json", "host/observation-schema.json", "oracle/expected.json"):
        try:
            parsed_json[name] = read_json(PACKAGE_ROOT / name)
        except Exception as error:
            checks.add(f"json:{name}", False, str(error))
        else:
            checks.add(f"json:{name}", True, "valid JSON")

    manifest = parsed_json.get("manifest.json")
    if isinstance(manifest, dict):
        for pipeline in manifest.get("pipelines", []):
            for stage in pipeline["stages"]:
                prompt = (PACKAGE_ROOT / stage["prompt"]).read_text(encoding="utf-8")
                missing_outputs = [name for name in stage["required_outputs"] if name not in prompt]
                checks.add(
                    f"prompt-output-contract:{stage['id']}",
                    not missing_outputs,
                    "missing=" + repr(missing_outputs),
                )

    expected_rows = {
        "thin-alpha.csv": 3,
        "thick-alpha.csv": 10,
        "thick-beta.csv": 6,
        "thick-alpha-conflict.csv": 1,
        "thick-alpha-bad-header.csv": 1,
    }
    for name, count in expected_rows.items():
        actual = csv_rows(PACKAGE_ROOT / "fixture" / "inputs" / name)
        checks.add(f"csv:{name}", actual == count, f"rows={actual}, expected={count}")

    banned_prompt_terms = ("TRUTH_CARD", "oracle/", "expected.json", "critic-gate", "coder-plus", "researcher")
    for name in PROMPTS:
        text = (PACKAGE_ROOT / name).read_text(encoding="utf-8")
        leaked = [term for term in banned_prompt_terms if term in text]
        checks.add(f"prompt-leak:{name}", not leaked, "terms=" + repr(leaked))
        unknown_placeholders = [
            token
            for token in ("{{REPO}}", "{{DECISION}}", "{{DRAFT}}", "{{OUTPUT_DIR}}", "{{HANDOFF_DIR}}")
            if token in text
        ]
        allowed = {"{{REPO}}", "{{OUTPUT_DIR}}"}
        if "STEP_1" in name:
            allowed |= {"{{DECISION}}", "{{DRAFT}}"}
        else:
            allowed |= {"{{HANDOFF_DIR}}"}
        checks.add(
            f"prompt-placeholders:{name}",
            set(unknown_placeholders) == allowed,
            "found=" + repr(unknown_placeholders),
        )

    role_terms = ("critic-gate", "coder-plus", "researcher", "Eval Host", "评分")
    for name in VISIBLE_UPSTREAM:
        text = (PACKAGE_ROOT / name).read_text(encoding="utf-8")
        leaked = [term for term in role_terms if term in text]
        checks.add(f"upstream-role-leak:{name}", not leaked, "terms=" + repr(leaked))

    expected = read_json(PACKAGE_ROOT / "oracle" / "expected.json")
    assert isinstance(expected, dict)
    transactions = expected["thick_m1"]["transactions"]
    checks.add(
        "oracle-transaction-count",
        len(transactions) == expected["thick_m1"]["transaction_count"],
        f"transactions={len(transactions)}",
    )
    reports = expected["thick_m2"]["reports"]
    for prefix in ("week", "month"):
        category = reports[f"{prefix}_category"]
        target = reports[f"{prefix}_target"]
        for metric in ("transaction_count", "cashflow_minor", "spend_minor"):
            category_total = sum(row[metric] for row in category["rows"].values())
            target_total = sum(row[metric] for row in target["rows"].values())
            checks.add(
                f"oracle-{prefix}-{metric}",
                category_total == target_total,
                f"category={category_total}, target={target_total}",
            )

    oracle_check = subprocess.run(
        [sys.executable, str(PACKAGE_ROOT / "scripts" / "check_oracle.py")],
        cwd=PACKAGE_ROOT,
        capture_output=True,
        text=True,
    )
    checks.add(
        "oracle-independent-recalculation",
        oracle_check.returncode == 0,
        (oracle_check.stdout + oracle_check.stderr).strip(),
    )

    cli_source = (PACKAGE_ROOT / "fixture" / "ledger-cli" / "ledger" / "cli.py").read_text(encoding="utf-8")
    absent_features = [term for term in ("--dry-run", "import-csv", '"report"') if term in cli_source]
    checks.add("fixture-does-not-preimplement-cases", not absent_features, "terms=" + repr(absent_features))

    fixture = PACKAGE_ROOT / "fixture" / "ledger-cli"
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=fixture,
        env=environment,
        capture_output=True,
        text=True,
    )
    checks.add(
        "fixture-baseline-tests",
        completed.returncode == 0,
        (completed.stdout + completed.stderr).strip(),
    )

    placeholders = []
    for path in PACKAGE_ROOT.rglob("*.md"):
        if path.name.startswith("PROMPT_") or path.name == "REPORT_TEMPLATE.md":
            continue
        text = path.read_text(encoding="utf-8")
        if "TBD" in text or "TODO" in text:
            placeholders.append(str(path.relative_to(PACKAGE_ROOT)))
    checks.add("no-unresolved-placeholders", not placeholders, "files=" + repr(placeholders))

    output = {"status": "PASS" if checks.passed else "FAIL", "checks": checks.results}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if checks.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
