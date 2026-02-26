import py_compile
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class TestSkillPythonScriptsCompile(unittest.TestCase):
    def _compile(self, rel_path: str) -> None:
        src = REPO_ROOT / rel_path
        self.assertTrue(src.exists(), f"Missing {rel_path}")
        with tempfile.TemporaryDirectory() as td:
            cfile = Path(td) / (src.stem + ".pyc")
            py_compile.compile(str(src), cfile=str(cfile), doraise=True)

    def test_openhands_api_v1_compiles(self) -> None:
        self._compile("skills/openhands-api-v1/scripts/openhands_api_v1.py")

    def test_babysit_pr_watch_compiles(self) -> None:
        self._compile("skills/babysit-pr/scripts/gh_pr_watch.py")


if __name__ == "__main__":
    unittest.main()
