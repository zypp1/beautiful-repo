from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "standardize-dl-repo" / "scripts" / "audit_dl_repo.py"


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
def documented(x: int) -> int:
    """Return the input value."""
    return x


def missing_docstring(x):
    return x
''',
                encoding="utf-8",
            )

            stats = module.analyze_python_file(path)

        self.assertEqual(stats["public_defs"], 2)
        self.assertEqual(stats["missing_docstrings"], 1)
        self.assertEqual(stats["syntax_errors"], 0)

    def test_audit_missing_path_returns_error_code(self) -> None:
        module = load_module()

        code = module.audit(Path("__definitely_missing_repo__"))

        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
