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
        hyphenation_warning = (
            'LaTeX Warning: StyleChecker Warning: "one-fish" also appears as '
            '"one fish" in .\n/ci/integration_test.tex on line 4  on input '
            "line 7."
        )
        hyphenation_list = (
            "StyleChecker: Hyphenated words appearing in this document:^^M\n"
            "StyleChecker: one-fish appears 1 time^^M StyleChecker: fox-in "
            "appears 1 time^^M\n"
            "StyleChecker: in-socks appears 1 time^^M\n"
            "StyleChecker: fox-in-socks appears 2 times^^M\n"
            "StyleChecker: fox-in~socks appears 1 time^^M\n"
            "StyleChecker: fox~in-socks appears 1 time^^M\n"
            "StyleChecker: bricks-with-blocks appears 1 time^^M "
            "StyleChecker: ^^M"
        )
        acronym_warning = (
            "LaTeX Warning: StyleChecker Warning: The acronym GEAH is "
            "possibly undefined.  o\nn input line 7."
        )
        acronym_list = (
            "StyleChecker: Acronyms appearing in this document:^^M "
            "StyleChecker: GEAH:^^M\n"
            "StyleChecker: CPU: Central Processing Unit^^M\n"
            "StyleChecker: GPU: Graphical Processing Unit^^M "
            "StyleChecker: RAM:^^M\n"
            "StyleChecker: ^^M"
        )
        localization_warning = (
            "LaTeX Warning: StyleChecker Warning: Both US and UK spellings "
            "are used in the s\name document, please check the full build "
            "logs for details.  on input line 7."
        )
        localization_list = (
            "StyleChecker: US spellings used in this document:^^M\n"
            "StyleChecker: In ./ci/integration_test.tex, line 6 the "
            'spellings: "localization\n'
            '" appear^^M\n'
            "StyleChecker: In ./test/test_localization_error.tex, line 4 the "
            'spellings: "Ana\n'
            'lyze" appear^^M StyleChecker: UK spellings used in this '
            "document:^^M\n"
            "StyleChecker: In ./ci/integration_test.tex, line 6 the "
            'spellings: "localisation\n'
            '" appear^^M\n'
            "StyleChecker: In ./test/test_localization_error.tex, line 5 the "
            'spellings: "Ana\n'
            'lyse" appear^^M StyleChecker: ^^M'
        )
        proc = subprocess.run(
            ["xelatex", "-shell-escape", "ci/integration_test.tex"], timeout=60
        )
        self.assertEqual(proc.returncode, 0)
        with open("integration_test.log", "r") as out_f:
            build_log = out_f.read()
            self.assertIn(hyphenation_warning, build_log)
            self.assertIn(hyphenation_list, build_log)
            self.assertIn(acronym_warning, build_log)
            self.assertIn(acronym_list, build_log)
            self.assertIn(localization_warning, build_log)
            self.assertIn(localization_list, build_log)
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
