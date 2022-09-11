"""System integration tests: call stylechecker from latex and ensure the
behavior is correct."""


import os
import subprocess
import unittest


class TestLatexBuild(unittest.TestCase):
    """System integration test case."""

    def setUp(self) -> None:
        """Increase the size of strings we can compare."""
        self.maxDiff = 2048

    def test_smoke(self) -> None:
        """Smoke test of check_hyphenation.  Passing this is the bare minimum
        required."""
        proc = subprocess.run(
            ["xelatex", "-shell-escape", "ci/integration_test.tex"], timeout=60
        )
        self.assertEqual(proc.returncode, 0)
        with open("integration_test.log", "r") as out_f:
            build_log = out_f.read()
            self.assertTrue(os.path.isfile("hyphenations.warnings"))
            self.assertTrue(os.path.isfile("hyphenations.list"))
            self.assertTrue(os.path.isfile("acronyms.warnings"))
            self.assertTrue(os.path.isfile("acronyms.list"))
            self.assertTrue(os.path.isfile("localization.warnings"))
            self.assertTrue(os.path.isfile("localization.list"))
        cleanup_list = [
            "acronyms.list",
            "acronyms.warnings",
            "hyphenations.list",
            "hyphenations.warnings",
            "integration_test.aux",
            "integration_test.log",
            "integration_test.pdf",
            "localization.list",
            "localization.warnings",
            "std.out",
        ]
        for file in cleanup_list:
            os.remove(file)


if __name__ == "__main__":
    unittest.main()
