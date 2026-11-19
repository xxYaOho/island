from __future__ import annotations

from pathlib import Path
from typing import Any

from .alpha import read_alpha
from .store import load_ledger, save_ledger


def _source_key(transaction: dict[str, Any]) -> tuple[str, str, str]:
    return (
        transaction["bank"],
        transaction["account"],
        transaction["transaction_id"],
    )


def import_alpha(
    ledger_path: Path,
    csv_path: Path,
    account: str,
) -> dict[str, int]:
    ledger = load_ledger(ledger_path)
    existing_keys = {_source_key(item) for item in ledger["transactions"]}
    added = 0
    duplicates = 0

    for transaction in read_alpha(csv_path, account):
        key = _source_key(transaction)
        if key in existing_keys:
            duplicates += 1
            continue
        ledger["transactions"].append(transaction)
        existing_keys.add(key)
        added += 1

    if added:
        save_ledger(ledger_path, ledger)
    return {"added": added, "duplicates": duplicates}
