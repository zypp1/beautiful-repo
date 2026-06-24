from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "beautiful-repo" / "scripts" / "audit_dl_repo.py"


def load_module():
    spec = importlib.util.spec_from_file_location("audit_dl_repo", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditDlRepoTests(unittest.TestCase):
    def test_has_ci_detects_yaml_workflows(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "quality.yaml").write_text("name: quality\n", encoding="utf-8")

            self.assertTrue(module.has_ci(root))

    def test_python_analysis_counts_public_docstrings(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "model.py"
            path.write_text(
                '''
"""Model helpers for tests."""

def documented(x: int) -> int:
    """Return the normalized integer label value."""
    return x


def missing_docstring(x):
    return x
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["public_defs"], 2)
        self.assertEqual(stats["missing_docstrings"], 1)
        self.assertEqual(stats["missing_module_docstring"], 0)
        self.assertEqual(stats["syntax_errors"], 0)

    def test_python_analysis_ignores_nested_public_helpers(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "model.py"
            path.write_text(
                '''
"""Model helpers for tests."""

def documented(x: int) -> int:
    """Return the normalized integer label value."""
    def nested_helper(y):
        return y
    return nested_helper(x)
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["public_defs"], 1)
        self.assertEqual(stats["missing_docstrings"], 0)

    def test_python_analysis_counts_missing_module_docstrings(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dataset.py"
            path.write_text(
                '''
def load_batch(path):
    """Load an image batch tensor from a manifest path."""
    return path
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["module_docstring_expected"], 1)
        self.assertEqual(stats["missing_module_docstring"], 1)

    def test_python_analysis_skips_test_module_docstring_requirement(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test_model.py"
            path.write_text(
                '''
def test_forward():
    assert True
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["module_docstring_expected"], 0)
        self.assertEqual(stats["missing_module_docstring"], 0)
        self.assertEqual(stats["public_defs"], 0)
        self.assertEqual(stats["missing_docstrings"], 0)

    def test_python_analysis_flags_thin_docstrings(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "metrics.py"
            path.write_text(
                '''
"""Segmentation metric implementations."""

def compute_dice(logits, target):
    """Compute dice."""
    return logits


def compute_iou(logits, target):
    """Compute mean IoU from segmentation logits.

    Args:
        logits: Float tensor of shape ``(B, K, H, W)``.
        target: Integer tensor of shape ``(B, H, W)``.

    Returns:
        Scalar tensor containing mean IoU. Higher is better.
    """
    return logits
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["public_defs"], 2)
        self.assertEqual(stats["thin_docstrings"], 1)

    def test_python_analysis_flags_long_docstrings(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dataset.py"
            path.write_text(
                '''
"""Dataset module.

Line 2.
Line 3.
Line 4.
Line 5.
Line 6.
Line 7.
Line 8.
Line 9.
"""


def load_batch(path):
    """Load a batch from disk.

    Line 2.
    Line 3.
    Line 4.
    Line 5.
    Line 6.
    Line 7.
    Line 8.
    Line 9.
    Line 10.
    Line 11.
    Line 12.
    Line 13.
    Line 14.
    Line 15.
    """
    return path
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["long_module_docstrings"], 1)
        self.assertEqual(stats["long_public_docstrings"], 1)

    def test_python_analysis_flags_public_api_naming(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "model.py"
            path.write_text(
                '''
"""Model definitions."""

BAD_CONST = 1


class bad_model:
    """Segmentation model used in naming tests."""

    def BadForward(self):
        return None


def RunModel(images):
    """Run model inference for an image tensor batch."""
    return images
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["bad_class_names"], 1)
        self.assertEqual(stats["bad_function_names"], 1)
        self.assertEqual(stats["bad_method_names"], 1)
        self.assertEqual(stats["bad_constant_names"], 0)

    def test_path_name_analysis_flags_directory_file_and_shadow_names(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BadDir").mkdir()
            (root / "src").mkdir()
            (root / "src" / "MyModel.py").write_text('"""Model file."""\n', encoding="utf-8")
            (root / "src" / "torch.py").write_text('"""Shadow file."""\n', encoding="utf-8")
            (root / "outputs" / "final").mkdir(parents=True)

            stats = module.analyze_path_names(root)

        self.assertEqual(stats["bad_dir_names"], 1)
        self.assertEqual(stats["bad_python_file_names"], 1)
        self.assertEqual(stats["shadow_python_file_names"], 1)
        self.assertEqual(stats["scratch_path_names"], 1)

    def test_test_files_do_not_count_public_api_naming(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test_model.py"
            path.write_text(
                '''
def TestForward():
    assert True
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["bad_function_names"], 0)

    def test_early_quickstart_requires_heading(self) -> None:
        module = load_module()

        prose_only = "This project has a quickstart coming soon.\n\n## Installation\n..."
        heading = "# Project\n\n## Quickstart\n```bash\npython demo.py\n```\n"

        self.assertFalse(module.has_early_quickstart(prose_only))
        self.assertTrue(module.has_early_quickstart(heading))

    def test_audit_missing_path_returns_error_code(self) -> None:
        module = load_module()

        code = module.audit(Path("__definitely_missing_repo__"))

        self.assertEqual(code, 2)

    def test_audit_treats_docs_and_citation_as_optional(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Project\n\n## Quickstart\nrun\n\n## Installation\ninstall\n\n"
                "## Data\ndata\n\n## Training\ntrain\n",
                encoding="utf-8",
            )
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
            (root / ".gitignore").write_text("data/\noutputs/\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            (root / "configs").mkdir()
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
            (root / "requirements.txt").write_text("torch\n", encoding="utf-8")
            (root / "scripts" / "train.py").write_text('"""Train entrypoint."""\n', encoding="utf-8")
            (root / "tests" / "test_imports.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

            buffer = io.StringIO()
            with redirect_stdout(buffer):
                module.audit(root)
            output = buffer.getvalue()

        self.assertNotIn("MISSING: docs", output)
        self.assertNotIn("MISSING: citation", output)
        self.assertIn("no: docs directory", output)
        self.assertIn("no: citation metadata", output)


if __name__ == "__main__":
    unittest.main()
