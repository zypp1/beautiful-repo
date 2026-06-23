#!/usr/bin/env python3
"""Audit a deep learning repository for reproducibility and release readiness."""

from __future__ import annotations

import argparse
import ast
import keyword
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
PYTHON_SHADOW_MODULES = {
    "argparse",
    "collections",
    "dataclasses",
    "json",
    "logging",
    "math",
    "numpy",
    "pathlib",
    "random",
    "re",
    "torch",
    "typing",
}
BAD_SCRATCH_NAME_WORDS = {
    "backup",
    "debug",
    "final",
    "latest",
    "misc",
    "new",
    "old",
    "scratch",
    "temp",
    "testnew",
    "tmp",
}
THIN_DOCSTRING_WORDS = {
    "calculate",
    "compute",
    "data",
    "do",
    "handle",
    "helper",
    "process",
    "run",
    "train",
    "util",
    "utilities",
    "utility",
    "wrapper",
}
DL_CONTRACT_WORDS = {
    "batch",
    "checkpoint",
    "config",
    "device",
    "dtype",
    "logit",
    "mask",
    "metric",
    "shape",
    "tensor",
}
MAX_MODULE_DOCSTRING_LINES = 8
MAX_PUBLIC_DOCSTRING_LINES = 14


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


def iter_relevant_dirs(root: Path) -> list[Path]:
    """Return repository directories that should participate in naming checks."""
    dirs: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_dir():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        dirs.append(path)
    return sorted(dirs)


def is_snake_case(name: str) -> bool:
    """Return whether a Python identifier uses lower snake_case."""
    return bool(re.fullmatch(r"[a-z_][a-z0-9_]*", name)) and not keyword.iskeyword(name)


def is_upper_snake_case(name: str) -> bool:
    """Return whether a Python identifier uses UPPER_SNAKE_CASE."""
    return bool(re.fullmatch(r"[A-Z_][A-Z0-9_]*", name))


def is_capwords(name: str) -> bool:
    """Return whether a class name follows CapWords closely enough for an audit."""
    return bool(re.fullmatch(r"[A-Z][A-Za-z0-9]*", name)) and "_" not in name


def is_kebab_or_snake_segment(name: str) -> bool:
    """Return whether a non-package directory segment is readable and lowercase."""
    return bool(re.fullmatch(r"[a-z0-9]+([_-][a-z0-9]+)*", name))


def has_scratch_name(name: str) -> bool:
    """Return whether a path segment looks like a scratch or local-only name."""
    compact = re.sub(r"[^a-z0-9]+", "", name.lower())
    words = set(re.split(r"[^a-z0-9]+", name.lower()))
    return compact in BAD_SCRATCH_NAME_WORDS or bool(words & BAD_SCRATCH_NAME_WORDS)


def analyze_path_names(root: Path) -> dict[str, int]:
    """Analyze directory and Python file naming conventions."""
    stats = {
        "bad_dir_names": 0,
        "bad_python_file_names": 0,
        "shadow_python_file_names": 0,
        "scratch_path_names": 0,
    }

    for path in iter_relevant_dirs(root):
        rel_parts = path.relative_to(root).parts
        name = path.name
        if name == ".":
            continue
        if name.startswith("."):
            continue
        if not is_kebab_or_snake_segment(name):
            stats["bad_dir_names"] += 1
        if has_scratch_name(name):
            stats["scratch_path_names"] += 1

    for path in iter_python_files(root):
        name = path.stem
        if name != "__init__" and not is_snake_case(name):
            stats["bad_python_file_names"] += 1
        if name in PYTHON_SHADOW_MODULES:
            stats["shadow_python_file_names"] += 1
        if has_scratch_name(name):
            stats["scratch_path_names"] += 1

    return stats


def normalize_identifier(text: str) -> str:
    """Normalize text for loose docstring/name comparisons."""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def public_name_tokens(name: str) -> set[str]:
    """Return meaningful tokens from a Python public object name."""
    return {
        token
        for token in re.split(r"[^a-zA-Z0-9]+|(?<=[a-z])(?=[A-Z])", name)
        if token and token != "_"
    }


def first_docstring_line(docstring: str) -> str:
    """Return the first non-empty docstring line."""
    for line in docstring.strip().splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def docstring_line_count(docstring: str) -> int:
    """Return the number of non-empty lines in a cleaned docstring."""
    return sum(1 for line in docstring.splitlines() if line.strip())


def is_thin_docstring(name: str, docstring: str, has_signature_detail: bool) -> bool:
    """Return whether a public docstring looks too vague to be useful."""
    first_line = normalize_identifier(first_docstring_line(docstring))
    if not first_line:
        return True

    words = first_line.split()
    if len(words) < 5 and has_signature_detail:
        return True

    name_tokens = {token.lower() for token in public_name_tokens(name)}
    if name_tokens and set(words).issubset(name_tokens | {"a", "an", "the", "to"}):
        return True

    if any(word in THIN_DOCSTRING_WORDS for word in words):
        has_domain_signal = any(
            word in DL_CONTRACT_WORDS for word in normalize_identifier(docstring).split()
        )
        if not has_domain_signal and len(words) <= 8:
            return True

    placeholder_patterns = [
        r":param\s+\w+\s*:\s*(todo|tbd|none)?\s*$",
        r"\b(todo|tbd|fixme)\b",
    ]
    normalized = docstring.lower()
    return any(
        re.search(pattern, normalized, flags=re.MULTILINE) for pattern in placeholder_patterns
    )


def is_test_file(path: Path) -> bool:
    """Return whether a file should be treated as test code."""
    return path.name.startswith("test_") or any(part == "tests" for part in path.parts)


def should_expect_module_docstring(path: Path) -> bool:
    """Return whether a Python file should normally have a module docstring."""
    if path.name == "__init__.py":
        return False
    if is_test_file(path):
        return False
    return True


def analyze_python_file(path: Path) -> dict[str, int]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return {
            "syntax_errors": 1,
            "module_docstring_expected": 0,
            "missing_module_docstring": 0,
            "long_module_docstrings": 0,
            "public_defs": 0,
            "missing_docstrings": 0,
            "thin_docstrings": 0,
            "long_public_docstrings": 0,
            "typed_defs": 0,
            "vague_names": 0,
            "bad_function_names": 0,
            "bad_method_names": 0,
            "bad_class_names": 0,
            "bad_constant_names": 0,
            "import_time_calls": 0,
        }

    module_docstring_expected = int(should_expect_module_docstring(path))
    module_docstring = ast.get_docstring(tree)
    missing_module_docstring = int(module_docstring_expected and not module_docstring)
    long_module_docstrings = int(
        bool(module_docstring)
        and docstring_line_count(module_docstring) > MAX_MODULE_DOCSTRING_LINES
    )
    count_public_api = not is_test_file(path)
    public_defs = 0
    missing_docstrings = 0
    thin_docstrings = 0
    long_public_docstrings = 0
    typed_defs = 0
    vague_names = 0
    bad_function_names = 0
    bad_method_names = 0
    bad_class_names = 0
    bad_constant_names = 0
    import_time_calls = 0

    for node in tree.body:
        if not count_public_api:
            break
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if node.name.startswith("_"):
            continue
        public_defs += 1
        if isinstance(node, ast.ClassDef):
            if not is_capwords(node.name):
                bad_class_names += 1
            for item in node.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                if item.name.startswith("_"):
                    continue
                if not is_snake_case(item.name):
                    bad_method_names += 1
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not is_snake_case(
            node.name
        ):
            bad_function_names += 1
        docstring = ast.get_docstring(node)
        if not docstring:
            missing_docstrings += 1
        else:
            has_signature_detail = isinstance(node, ast.ClassDef) or bool(
                getattr(node, "args", None) and (
                    node.args.posonlyargs
                    or node.args.args
                    or node.args.kwonlyargs
                    or node.args.vararg
                    or node.args.kwarg
                )
            )
            if is_thin_docstring(node.name, docstring, has_signature_detail):
                thin_docstrings += 1
            if docstring_line_count(docstring) > MAX_PUBLIC_DOCSTRING_LINES:
                long_public_docstrings += 1
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            has_return = node.returns is not None
            has_arg_hints = all(
                arg.annotation is not None
                for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
                if arg.arg not in {"self", "cls"}
            )
            if has_return or has_arg_hints:
                typed_defs += 1

    if not is_test_file(path):
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        if not is_upper_snake_case(target.id):
                            bad_constant_names += 1
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
        "module_docstring_expected": module_docstring_expected,
        "missing_module_docstring": missing_module_docstring,
        "long_module_docstrings": long_module_docstrings,
        "public_defs": public_defs,
        "missing_docstrings": missing_docstrings,
        "thin_docstrings": thin_docstrings,
        "long_public_docstrings": long_public_docstrings,
        "typed_defs": typed_defs,
        "vague_names": vague_names,
        "bad_function_names": bad_function_names,
        "bad_method_names": bad_method_names,
        "bad_class_names": bad_class_names,
        "bad_constant_names": bad_constant_names,
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
        "module_docstring_expected": 0,
        "missing_module_docstring": 0,
        "long_module_docstrings": 0,
        "public_defs": 0,
        "missing_docstrings": 0,
        "thin_docstrings": 0,
        "long_public_docstrings": 0,
        "typed_defs": 0,
        "vague_names": 0,
        "bad_function_names": 0,
        "bad_method_names": 0,
        "bad_class_names": 0,
        "bad_constant_names": 0,
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
    module_docstring_ratio = (
        1.0 - (py_stats["missing_module_docstring"] / py_stats["module_docstring_expected"])
        if py_stats["module_docstring_expected"]
        else 1.0
    )
    thin_docstring_ratio = (
        py_stats["thin_docstrings"] / py_stats["public_defs"] if py_stats["public_defs"] else 0.0
    )
    long_docstring_hits = py_stats["long_module_docstrings"] + py_stats["long_public_docstrings"]
    path_name_stats = analyze_path_names(root)
    naming_hits = (
        path_name_stats["bad_dir_names"]
        + path_name_stats["bad_python_file_names"]
        + path_name_stats["shadow_python_file_names"]
        + path_name_stats["scratch_path_names"]
        + py_stats["bad_function_names"]
        + py_stats["bad_method_names"]
        + py_stats["bad_class_names"]
        + py_stats["bad_constant_names"]
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
        ("module docstrings", module_docstring_ratio >= 0.8),
        ("public API docstrings", docstring_ratio >= 0.5),
        ("limited thin docstrings", thin_docstring_ratio <= 0.2),
        ("concise docstrings", long_docstring_hits == 0),
        (
            "directory and file naming",
            path_name_stats["bad_dir_names"] == 0
            and path_name_stats["bad_python_file_names"] == 0,
        ),
        ("no import-shadowing Python file names", path_name_stats["shadow_python_file_names"] == 0),
        (
            "public API naming",
            py_stats["bad_function_names"] == 0
            and py_stats["bad_method_names"] == 0
            and py_stats["bad_class_names"] == 0
            and py_stats["bad_constant_names"] == 0,
        ),
        ("limited scratch names", path_name_stats["scratch_path_names"] <= 1),
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
    print(f"- modules expected to have docstrings: {py_stats['module_docstring_expected']}")
    print(f"- modules missing docstrings: {py_stats['missing_module_docstring']}")
    print(f"- long module docstrings: {py_stats['long_module_docstrings']}")
    print(f"- public definitions: {py_stats['public_defs']}")
    print(f"- public definitions missing docstrings: {py_stats['missing_docstrings']}")
    print(f"- thin public docstrings: {py_stats['thin_docstrings']}")
    print(f"- long public docstrings: {py_stats['long_public_docstrings']}")
    print(f"- typed public functions/classes: {py_stats['typed_defs']}")
    print(f"- directories with nonstandard names: {path_name_stats['bad_dir_names']}")
    print(f"- Python files with non-snake-case names: {path_name_stats['bad_python_file_names']}")
    print(f"- Python files shadowing common modules: {path_name_stats['shadow_python_file_names']}")
    print(f"- public functions with non-snake-case names: {py_stats['bad_function_names']}")
    print(f"- public methods with non-snake-case names: {py_stats['bad_method_names']}")
    print(f"- public classes with non-CapWords names: {py_stats['bad_class_names']}")
    print(f"- public constants with non-UPPER-SNAKE names: {py_stats['bad_constant_names']}")
    print(f"- scratch-like path names: {path_name_stats['scratch_path_names']}")
    print(f"- total naming issue hints: {naming_hits}")
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
