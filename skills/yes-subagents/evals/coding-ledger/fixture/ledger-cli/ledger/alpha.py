from __future__ import annotations

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {"交易时间", "交易单号", "交易对象", "类型", "金额", "分类"}
CATEGORIES = {"餐饮", "日用", "收入", "转账"}
KINDS = {"支出": "expense", "收入": "income", "退款": "refund"}


def _normalize_space(value: str) -> str:
    return " ".join(value.strip().split())


def _amount_minor(value: str, kind: str) -> int:
    amount = int((Decimal(value) * 100).to_integral_exact())
    return -abs(amount) if kind == "expense" else abs(amount)


def _occurred_at(value: str) -> str:
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError("交易时间必须带时区")
    return parsed.isoformat()


def read_alpha(path: Path, account: str) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not REQUIRED_FIELDS.issubset(reader.fieldnames):
            raise ValueError("Alpha CSV 缺少必需表头")

        transactions: list[dict[str, Any]] = []
        for row_number, row in enumerate(reader, start=2):
            kind = KINDS[row["类型"].strip()]
            category = row["分类"].strip()
            transactions.append(
                {
                    "bank": "alpha",
                    "account": account,
                    "transaction_id": row["交易单号"].strip(),
                    "occurred_at": _occurred_at(row["交易时间"].strip()),
                    "amount_minor": _amount_minor(row["金额"].strip(), kind),
                    "currency": "CNY",
                    "kind": kind,
                    "target": _normalize_space(row["交易对象"]),
                    "category": category if category in CATEGORIES else "未分类",
                    "source": {
                        "file": path.name,
                        "row": row_number,
                        "raw": row,
                    },
                }
            )
    return transactions
