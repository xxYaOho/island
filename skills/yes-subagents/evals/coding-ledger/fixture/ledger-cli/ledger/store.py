from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_ledger(path: Path) -> dict[str, list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("transactions"), list):
        raise ValueError("ledger must contain a transactions array")
    return payload


def save_ledger(path: Path, ledger: dict[str, list[dict[str, Any]]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
