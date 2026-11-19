from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .service import import_alpha
from .store import load_ledger


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ledger")
    commands = parser.add_subparsers(dest="command", required=True)

    list_command = commands.add_parser("list")
    list_command.add_argument("--ledger", type=Path, required=True)

    import_command = commands.add_parser("import-alpha")
    import_command.add_argument("--ledger", type=Path, required=True)
    import_command.add_argument("--account", required=True)
    import_command.add_argument("--file", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "list":
        result = load_ledger(args.ledger)
    else:
        result = import_alpha(args.ledger, args.file, args.account)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
