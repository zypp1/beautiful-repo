from __future__ import annotations

import importlib.util
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
