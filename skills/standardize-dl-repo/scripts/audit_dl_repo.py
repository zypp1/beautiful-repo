#!/usr/bin/env python3
"""Audit a deep learning repository for reproducibility and release readiness."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT_FILES = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "pyproject.toml",
    ".gitignore",
]

QUALITY_FILES = [
    ".pre-commit-config.yaml",
    ".github/workflows/quality.yml",
    ".github/workflows/ci.yml",
]

TARGET_DIRS = [
    "configs",
    "src",
    "scripts",
    "tests",
    "docs",
    "examples",
]

ENTRYPOINTS = [
    "scripts/train.py",
    "scripts/eval.py",
    "scripts/infer.py",
    "scripts/export.py",
    "train.py",
    "eval.py",
    "infer.py",
]

ARTIFACT_DIRS = [
    "data",
    "datasets",
    "checkpoints",
    "weights",
    "runs",
    "wandb",
    "mlruns",
    "outputs",
    "logs",
    "lightning_logs",
]


def exists_any(root: Path, paths: list[str]) -> list[str]:
    return [path for path in paths if (root / path).exists()]


def list_matches(root: Path, patterns: list[str]) -> list[Path]:
    matches: list[Path] = []
    for pattern in patterns:
        matches.extend(root.glob(pattern))
    return sorted({path for path in matches if path.is_file()})


def has_ci(root: Path) -> bool:
    workflow_dir = root / ".github" / "workflows"
    return workflow_dir.exists() and any(workflow_dir.glob("*.yml")) or any(workflow_dir.glob("*.yaml")) if workflow_dir.exists() else False


def read_gitignore(root: Path) -> str:
    path = root / ".gitignore"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def audit(root: Path) -> int:
    root = root.resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: repository path does not exist or is not a directory: {root}")
        return 2

    present_root = exists_any(root, ROOT_FILES)
    present_dirs = exists_any(root, TARGET_DIRS)
    present_entrypoints = exists_any(root, ENTRYPOINTS)
    config_files = list_matches(root, ["configs/**/*.yaml", "configs/**/*.yml", "configs/**/*.json", "*.yaml", "*.yml"])
    notebooks = list_matches(root, ["**/*.ipynb"])
    tests = list_matches(root, ["tests/test_*.py", "test_*.py", "**/test_*.py"])
    dependency_files = exists_any(root, ["requirements.txt", "environment.yml", "conda.yml", "uv.lock", "poetry.lock", "Pipfile.lock"])
    ci_present = has_ci(root)

    gitignore = read_gitignore(root)
    ignored_artifacts = [name for name in ARTIFACT_DIRS if name in gitignore]
    existing_artifacts = [name for name in ARTIFACT_DIRS if (root / name).exists()]

    checks = [
        ("README", "README.md" in present_root),
        ("license", "LICENSE" in present_root),
        ("citation", "CITATION.cff" in present_root),
        ("pyproject", "pyproject.toml" in present_root),
        ("dependency lock or spec", bool(dependency_files)),
        ("configs directory or config files", "configs" in present_dirs or bool(config_files)),
        ("script entrypoints", bool(present_entrypoints)),
        ("src package layout", "src" in present_dirs),
        ("tests", bool(tests)),
        ("docs", "docs" in present_dirs),
        ("CI", ci_present),
        ("artifact ignore rules", bool(ignored_artifacts)),
    ]

    score = sum(1 for _, ok in checks if ok)
    total = len(checks)

    print(f"Repository: {root}")
    print(f"Score: {score}/{total}")
    print()
    print("Checks:")
    for name, ok in checks:
        marker = "OK" if ok else "MISSING"
        print(f"- {marker}: {name}")

    print()
    print("Detected:")
    print(f"- root files: {', '.join(present_root) if present_root else 'none'}")
    print(f"- dependency files: {', '.join(dependency_files) if dependency_files else 'none'}")
    print(f"- target dirs: {', '.join(present_dirs) if present_dirs else 'none'}")
    print(f"- entrypoints: {', '.join(present_entrypoints) if present_entrypoints else 'none'}")
    print(f"- config files: {len(config_files)}")
    print(f"- tests: {len(tests)}")
    print(f"- notebooks: {len(notebooks)}")
    print(f"- artifact dirs present: {', '.join(existing_artifacts) if existing_artifacts else 'none'}")
    print(f"- artifact dirs ignored: {', '.join(ignored_artifacts) if ignored_artifacts else 'none'}")

    missing = [name for name, ok in checks if not ok]
    if missing:
        print()
        print("Suggested next steps:")
        for item in missing[:6]:
            print(f"- Add or normalize: {item}")

    return 0 if score == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Repository path to audit")
    args = parser.parse_args()
    return audit(Path(args.repo))


if __name__ == "__main__":
    raise SystemExit(main())
