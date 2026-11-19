#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = PACKAGE_ROOT / "fixture" / "ledger-cli"
MANIFEST = json.loads((PACKAGE_ROOT / "manifest.json").read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def run_git(repo: Path, *args: str) -> None:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")


def prepare_case(run_root: Path, case: str) -> dict[str, object]:
    pipeline = next(item for item in MANIFEST["pipelines"] if item["id"] == case)
    case_root = run_root / case
    repo = case_root / "repo"
    upstream = case_root / "upstream"
    artifacts = case_root / "artifacts"

    shutil.copytree(
        FIXTURE_ROOT,
        repo,
        ignore=shutil.ignore_patterns(".DS_Store", "._*", "__pycache__", ".pytest_cache"),
    )
    upstream.mkdir(parents=True)
    for name in ("Decision.md", "Draft.md"):
        shutil.copy2(PACKAGE_ROOT / "cases" / case / name, upstream / name)

    input_root = repo / "eval-inputs"
    input_root.mkdir()
    for source in pipeline["input_files"]:
        name = Path(source).name
        shutil.copy2(PACKAGE_ROOT / "fixture" / "inputs" / name, input_root / name)

    for stage in pipeline["stages"]:
        (artifacts / stage["id"]).mkdir(parents=True)

    run_git(repo, "init", "-q")
    run_git(repo, "config", "user.name", "Eval Agent")
    run_git(repo, "config", "user.email", "eval-agent@example.invalid")
    run_git(repo, "add", ".")
    run_git(
        repo,
        "-c",
        "user.name=Eval Fixture",
        "-c",
        "user.email=eval@example.invalid",
        "commit",
        "-qm",
        "chore: initialize ledger eval fixture",
    )

    visible_files = [
        upstream / "Decision.md",
        upstream / "Draft.md",
        *sorted(
            path
            for path in repo.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and path.name != ".DS_Store"
            and "__pycache__" not in path.parts
            and ".pytest_cache" not in path.parts
        ),
    ]
    return {
        "case": case,
        "repo": str(repo),
        "upstream": str(upstream),
        "artifacts": str(artifacts),
        "visible_sha256": {
            str(path.relative_to(case_root)): sha256(path) for path in visible_files
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare isolated coding-ledger eval workspaces")
    parser.add_argument("run_root", type=Path)
    args = parser.parse_args()
    run_root = args.run_root.resolve()

    if run_root.exists():
        raise SystemExit(f"refusing to overwrite existing run root: {run_root}")

    run_root.mkdir(parents=True)
    try:
        cases = [prepare_case(run_root, case) for case in ("thin", "thick")]
        host = run_root / "host"
        host.mkdir()
        shutil.copy2(PACKAGE_ROOT / "host" / "observation-schema.json", host)
        shutil.copy2(PACKAGE_ROOT / "host" / "REPORT_TEMPLATE.md", host)
        manifest = {
            "package_id": "coding-ledger-v1",
            "package_manifest": str(PACKAGE_ROOT / "manifest.json"),
            "cases": cases,
        }
        (run_root / "run-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except Exception:
        # Preserve a partially prepared directory for diagnosis; never delete user paths.
        raise

    print(json.dumps({"status": "ready", "run_root": str(run_root)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
