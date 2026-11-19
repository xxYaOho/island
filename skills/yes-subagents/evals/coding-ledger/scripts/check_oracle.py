#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "fixture" / "inputs"
EXPECTED = json.loads((ROOT / "oracle" / "expected.json").read_text(encoding="utf-8"))
SEED = json.loads((ROOT / "fixture" / "ledger-cli" / "data" / "ledger.json").read_text(encoding="utf-8"))

CATEGORY_MAP = {
    "餐饮": "餐饮",
    "日用": "日用",
    "收入": "收入",
    "转账": "转账",
    "Dining": "餐饮",
    "Groceries": "日用",
    "Income": "收入",
    "Transfer": "转账",
}


def spaces(value: str) -> str:
    return " ".join(value.strip().split())


def cents(value: str) -> int:
    return int((Decimal(value) * 100).to_integral_exact())


def alpha(path: Path, account: str) -> tuple[list[dict[str, Any]], int]:
    transactions: list[dict[str, Any]] = []
    rejected = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            try:
                kind = {"支出": "expense", "收入": "income", "退款": "refund"}[row["类型"].strip()]
                amount = cents(row["金额"].strip())
                transaction = {
                    "bank": "alpha",
                    "account": account,
                    "transaction_id": row["交易单号"].strip(),
                    "occurred_at": datetime.fromisoformat(row["交易时间"].strip()).isoformat(),
                    "amount_minor": -abs(amount) if kind == "expense" else abs(amount),
                    "currency": "CNY",
                    "kind": kind,
                    "target": spaces(row["交易对象"]),
                    "category": CATEGORY_MAP.get(row["分类"].strip(), "未分类"),
                    "source": {"file": path.name, "row": row_number, "raw": row},
                }
            except (KeyError, ValueError, ArithmeticError):
                rejected += 1
            else:
                transactions.append(transaction)
    return transactions, rejected


def beta(path: Path, account: str) -> tuple[list[dict[str, Any]], int]:
    transactions: list[dict[str, Any]] = []
    rejected = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            try:
                debit = row["debit"].strip()
                credit = row["credit"].strip()
                if bool(debit) == bool(credit):
                    raise ValueError("exactly one of debit and credit is required")
                kind = {"Expense": "expense", "Income": "income", "Refund": "refund"}[row["type"].strip()]
                amount = cents(debit or credit)
                transaction = {
                    "bank": "beta",
                    "account": account,
                    "transaction_id": row["reference"].strip(),
                    "occurred_at": datetime.fromisoformat(row["posted_at"].strip()).isoformat(),
                    "amount_minor": -abs(amount) if kind == "expense" else abs(amount),
                    "currency": "CNY",
                    "kind": kind,
                    "target": spaces(row["description"]),
                    "category": CATEGORY_MAP.get(row["category"].strip(), "未分类"),
                    "source": {"file": path.name, "row": row_number, "raw": row},
                }
            except (KeyError, ValueError, ArithmeticError):
                rejected += 1
            else:
                transactions.append(transaction)
    return transactions, rejected


def key(item: dict[str, Any]) -> tuple[str, str, str]:
    return item["bank"], item["account"], item["transaction_id"]


def same_business(left: dict[str, Any], right: dict[str, Any]) -> bool:
    fields = ("occurred_at", "amount_minor", "currency", "kind", "target")
    return all(left[field] == right[field] for field in fields)


def reconcile(
    ledger: dict[tuple[str, str, str], dict[str, Any]],
    incoming: list[dict[str, Any]],
    rejected: int,
) -> dict[str, int]:
    result = {"added": 0, "duplicates": 0, "conflicts": 0, "rejected": rejected}
    for item in incoming:
        identity = key(item)
        if identity not in ledger:
            ledger[identity] = item
            result["added"] += 1
        elif same_business(ledger[identity], item):
            result["duplicates"] += 1
        else:
            result["conflicts"] += 1
    return result


def projection(item: dict[str, Any]) -> dict[str, Any]:
    source = item["source"]
    return {
        "occurred_at": item["occurred_at"],
        "amount_minor": item["amount_minor"],
        "currency": item["currency"],
        "kind": item["kind"],
        "target": item["target"],
        "category": item["category"],
        "source_file": source["file"],
        "source_row": source["row"],
    }


def period_bounds(period: str, anchor: str) -> tuple[date, date]:
    day = date.fromisoformat(anchor)
    if period == "week":
        start = day - timedelta(days=day.weekday())
        return start, start + timedelta(days=7)
    start = day.replace(day=1)
    end = date(start.year + (start.month == 12), 1 if start.month == 12 else start.month + 1, 1)
    return start, end


def report(
    ledger: dict[tuple[str, str, str], dict[str, Any]],
    period: str,
    anchor: str,
    group_by: str,
) -> dict[str, Any]:
    start, end = period_bounds(period, anchor)
    rows: dict[str, dict[str, int]] = {}
    for item in ledger.values():
        occurred = datetime.fromisoformat(item["occurred_at"]).date()
        if not start <= occurred < end:
            continue
        group = item[group_by]
        row = rows.setdefault(
            group,
            {"transaction_count": 0, "cashflow_minor": 0, "spend_minor": 0},
        )
        row["transaction_count"] += 1
        row["cashflow_minor"] += item["amount_minor"]
        if item["kind"] == "expense":
            row["spend_minor"] += abs(item["amount_minor"])
        elif item["kind"] == "refund":
            row["spend_minor"] -= abs(item["amount_minor"])
    return {"period_start": start.isoformat(), "period_end": end.isoformat(), "rows": rows}


def main() -> int:
    ledger = {key(item): item for item in SEED["transactions"]}
    alpha_rows, alpha_rejected = alpha(INPUTS / "thick-alpha.csv", "alpha-main")
    beta_rows, beta_rejected = beta(INPUTS / "thick-beta.csv", "beta-card")
    conflict_rows, conflict_rejected = alpha(INPUTS / "thick-alpha-conflict.csv", "alpha-main")

    actual_imports = {
        "alpha_primary": reconcile(ledger, alpha_rows, alpha_rejected),
        "beta_primary": reconcile(ledger, beta_rows, beta_rejected),
        "alpha_repeat": reconcile(ledger, alpha_rows, alpha_rejected),
        "alpha_conflict": reconcile(ledger, conflict_rows, conflict_rejected),
    }
    wanted_m1 = EXPECTED["thick_m1"]
    actual_transactions = {"|".join(identity): projection(item) for identity, item in ledger.items()}

    actual_reports = {
        "week_category": report(ledger, "week", "2026-09-03", "category"),
        "week_target": report(ledger, "week", "2026-09-03", "target"),
        "month_category": report(ledger, "month", "2026-09-15", "category"),
        "month_target": report(ledger, "month", "2026-09-15", "target"),
    }
    checks = {
        "imports": actual_imports == wanted_m1["imports"],
        "transaction_count": len(ledger) == wanted_m1["transaction_count"],
        "transactions": actual_transactions == wanted_m1["transactions"],
        "reports": actual_reports == EXPECTED["thick_m2"]["reports"],
    }
    print(json.dumps({"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}, ensure_ascii=False))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
