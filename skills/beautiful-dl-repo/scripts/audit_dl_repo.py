#!/usr/bin/env python3
"""Audit a deep learning repository for reproducibility and release readiness."""

from __future__ import annotations

import argparse
import ast
import re
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

README_SECTIONS = [
    "installation",
    "quickstart",
    "data",
    "training",
    "evaluation",
    "inference",
    "results",
    "citation",
    "license",
]

README_VISUAL_TOKENS = ["![", "<img", ".png", ".jpg", ".jpeg", ".gif", ".webp"]
README_CARD_TOKENS = ["<table", "<td", "<div", "width=\"33%\"", "width=\"900\""]
README_BADGE_TOKENS = ["img.shields.io", "badge.svg", "badge/", "badge?"]
README_GALLERY_TOKENS = ["gallery", "examples", "screenshots", "demo gif", "qualitative"]
README_LINK_TARGETS = [
    "paper",
    "project page",
    "demo",
    "docs",
    "checkpoints",
    "dataset",
    "citation",
]
README_DEAD_PLACEHOLDERS = [
    "replace_or_remove",
    'href="#"',
    "https://project-page.example",
    "https://arxiv.org/abs/...",
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

CODE_QUALITY_FILES = [
    ".pre-commit-config.yaml",
    "ruff.toml",
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

VAGUE_NAMES = {"foo", "bar", "tmp", "res", "obj", "thing"}
IMPORT_TIME_CALLS = {"train", "evaluate", "download", "load_checkpoint", "fit"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "build", "dist"}


def exists_any(root: Path, paths: list[str]) -> list[str]:
    return [path for path in paths if (root / path).exists()]


def list_matches(root: Path, patterns: list[str]) -> list[Path]:
    matches: list[Path] = []
    for pattern in patterns:
        matches.extend(root.glob(pattern))
    return sorted({path for path in matches if path.is_file()})


def has_ci(root: Path) -> bool:
    workflow_dir = root / ".github" / "workflows"
    if not workflow_dir.exists():
        return False
    return any(workflow_dir.glob("*.yml")) or any(workflow_dir.glob("*.yaml"))


def read_gitignore(root: Path) -> str:
    path = root / ".gitignore"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def read_readme(root: Path) -> str:
    path = root / "README.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore").lower()


def markdown_headings(text: str) -> list[tuple[int, str, int]]:
    """Return Markdown ATX headings as ``(level, title, start_index)`` tuples."""
    headings: list[tuple[int, str, int]] = []
    pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        raw_title = re.sub(r"<[^>]+>", "", match.group(2))
        title = re.sub(r"\s+", " ", raw_title).strip().lower()
        headings.append((len(match.group(1)), title, match.start()))
    return headings


def heading_position(headings: list[tuple[int, str, int]], keywords: list[str]) -> int | None:
    """Return the first heading offset containing any keyword."""
    for _, title, start in headings:
        if any(keyword in title for keyword in keywords):
            return start
    return None


def has_early_quickstart(readme: str) -> bool:
    """Detect a real Quickstart heading near the top of a README."""
    headings = markdown_headings(readme)
    quickstart_pos = heading_position(headings, ["quickstart", "quick start", "getting started"])
    if quickstart_pos is None:
        return False
    installation_pos = heading_position(headings, ["installation", "install", "setup"])
    if installation_pos is None:
        return quickstart_pos <= 4000
    return quickstart_pos <= installation_pos + 2000


def iter_python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def analyze_python_file(path: Path) -> dict[str, int]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return {
            "syntax_errors": 1,
            "public_defs": 0,
            "missing_docstrings": 0,
            "typed_defs": 0,
            "vague_names": 0,
            "import_time_calls": 0,
        }

    public_defs = 0
    missing_docstrings = 0
    typed_defs = 0
    vague_names = 0
    import_time_calls = 0

    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if node.name.startswith("_"):
            continue
        public_defs += 1
        if not ast.get_docstring(node):
            missing_docstrings += 1
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            has_return = node.returns is not None
            has_arg_hints = all(
                arg.annotation is not None
                for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
                if arg.arg not in {"self", "cls"}
            )
            if has_return or has_arg_hints:
                typed_defs += 1

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in VAGUE_NAMES:
            vague_names += 1

    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            func = node.value.func
            name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
            if name in IMPORT_TIME_CALLS:
                import_time_calls += 1
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            func = node.value.func
            name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
            if name in IMPORT_TIME_CALLS:
                import_time_calls += 1

    return {
        "syntax_errors": 0,
        "public_defs": public_defs,
        "missing_docstrings": missing_docstrings,
        "typed_defs": typed_defs,
        "vague_names": vague_names,
        "import_time_calls": import_time_calls,
    }


def audit(root: Path) -> int:
    root = root.resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: repository path does not exist or is not a directory: {root}")
        return 2

    present_root = exists_any(root, ROOT_FILES)
    present_dirs = exists_any(root, TARGET_DIRS)
    present_entrypoints = exists_any(root, ENTRYPOINTS)
    config_files = list_matches(
        root,
        ["configs/**/*.yaml", "configs/**/*.yml", "configs/**/*.json", "*.yaml", "*.yml"],
    )
    notebooks = list_matches(root, ["**/*.ipynb"])
    tests = list_matches(root, ["tests/test_*.py", "test_*.py", "**/test_*.py"])
    dependency_files = exists_any(
        root,
        [
            "requirements.txt",
            "environment.yml",
            "conda.yml",
            "uv.lock",
            "poetry.lock",
            "Pipfile.lock",
        ],
    )
    ci_present = has_ci(root)
    code_quality_files = exists_any(root, CODE_QUALITY_FILES)

    gitignore = read_gitignore(root)
    readme = read_readme(root)
    ignored_artifacts = [name for name in ARTIFACT_DIRS if name in gitignore]
    existing_artifacts = [name for name in ARTIFACT_DIRS if (root / name).exists()]
    readme_sections = [section for section in README_SECTIONS if section in readme]
    readme_has_visual = any(token in readme for token in README_VISUAL_TOKENS)
    readme_has_cards = any(token in readme for token in README_CARD_TOKENS)
    readme_has_badges = any(token in readme for token in README_BADGE_TOKENS)
    readme_has_gallery = any(token in readme for token in README_GALLERY_TOKENS)
    readme_has_centered_hero = "<div align=\"center\"" in readme or "<p align=\"center\"" in readme
    readme_has_links = readme.count("](") >= 3 or readme.count("<a ") >= 3
    readme_link_targets = [target for target in README_LINK_TARGETS if target in readme]
    readme_has_link_hub = len(readme_link_targets) >= 4
    readme_has_checkpoint_signal = any(
        token in readme for token in ["checkpoint", "pretrained", "model zoo", "weights"]
    )
    readme_has_result_signal = any(
        token in readme
        for token in ["result", "benchmark", "metric", "miou", "map", "accuracy", "dice"]
    )
    readme_has_early_quickstart = has_early_quickstart(readme)
    readme_has_dead_placeholders = any(token in readme for token in README_DEAD_PLACEHOLDERS)
    python_files = iter_python_files(root)
    py_stats = {
        "syntax_errors": 0,
        "public_defs": 0,
        "missing_docstrings": 0,
        "typed_defs": 0,
        "vague_names": 0,
        "import_time_calls": 0,
    }
    for path in python_files:
        stats = analyze_python_file(path)
        for key, value in stats.items():
            py_stats[key] += value

    docstring_ratio = (
        1.0 - (py_stats["missing_docstrings"] / py_stats["public_defs"])
        if py_stats["public_defs"]
        else 1.0
    )

    checks = [
        ("README", "README.md" in present_root),
        ("README core sections", len(readme_sections) >= 5),
        ("README visual or link hub", readme_has_visual or readme_has_links),
        ("README card-style first screen", readme_has_cards and readme_has_visual),
        ("README centered hero", readme_has_centered_hero),
        ("README badges", readme_has_badges),
        ("README gallery/examples signal", readme_has_gallery or readme_has_visual),
        ("README early quickstart", readme_has_early_quickstart),
        ("README research link hub", readme_has_link_hub),
        ("README checkpoint/model signal", readme_has_checkpoint_signal),
        ("README result signal", readme_has_result_signal),
        ("README no dead placeholders", not readme_has_dead_placeholders),
        ("license", "LICENSE" in present_root),
        ("citation", "CITATION.cff" in present_root),
        ("pyproject", "pyproject.toml" in present_root),
        ("dependency lock or spec", bool(dependency_files)),
        ("code quality config", "pyproject.toml" in present_root or bool(code_quality_files)),
        ("configs directory or config files", "configs" in present_dirs or bool(config_files)),
        ("script entrypoints", bool(present_entrypoints)),
        ("src package layout", "src" in present_dirs),
        ("tests", bool(tests)),
        ("docs", "docs" in present_dirs),
        ("CI", ci_present),
        ("artifact ignore rules", bool(ignored_artifacts)),
        ("Python syntax", py_stats["syntax_errors"] == 0),
        ("public API docstrings", docstring_ratio >= 0.5),
        ("limited vague names", py_stats["vague_names"] <= max(5, len(python_files))),
        ("limited import-time side effects", py_stats["import_time_calls"] == 0),
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
    print(
        f"- code quality files: {', '.join(code_quality_files) if code_quality_files else 'none'}"
    )
    print(f"- target dirs: {', '.join(present_dirs) if present_dirs else 'none'}")
    print(f"- entrypoints: {', '.join(present_entrypoints) if present_entrypoints else 'none'}")
    print(f"- config files: {len(config_files)}")
    print(f"- tests: {len(tests)}")
    print(f"- notebooks: {len(notebooks)}")
    print(f"- README sections: {', '.join(readme_sections) if readme_sections else 'none'}")
    print(f"- README visual signal: {'yes' if readme_has_visual else 'no'}")
    print(f"- README card signal: {'yes' if readme_has_cards else 'no'}")
    print(f"- README centered hero: {'yes' if readme_has_centered_hero else 'no'}")
    print(f"- README badges: {'yes' if readme_has_badges else 'no'}")
    print(f"- README gallery/examples signal: {'yes' if readme_has_gallery else 'no'}")
    print(f"- README early quickstart: {'yes' if readme_has_early_quickstart else 'no'}")
    link_targets = ", ".join(readme_link_targets) if readme_link_targets else "none"
    print(f"- README link targets: {link_targets}")
    print(f"- README checkpoint/model signal: {'yes' if readme_has_checkpoint_signal else 'no'}")
    print(f"- README result signal: {'yes' if readme_has_result_signal else 'no'}")
    print(f"- README dead placeholders: {'yes' if readme_has_dead_placeholders else 'no'}")
    print(f"- Python files: {len(python_files)}")
    print(f"- public definitions: {py_stats['public_defs']}")
    print(f"- public definitions missing docstrings: {py_stats['missing_docstrings']}")
    print(f"- typed public functions/classes: {py_stats['typed_defs']}")
    print(f"- vague variable-name hits: {py_stats['vague_names']}")
    print(f"- possible import-time side-effect calls: {py_stats['import_time_calls']}")
    artifact_dirs = ", ".join(existing_artifacts) if existing_artifacts else "none"
    ignored_dirs = ", ".join(ignored_artifacts) if ignored_artifacts else "none"
    print(f"- artifact dirs present: {artifact_dirs}")
    print(f"- artifact dirs ignored: {ignored_dirs}")

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
