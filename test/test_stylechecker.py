"""Unit test cases for the booking module."""


from typing import Dict, NamedTuple


import os
import sys
import unittest


sys.path.append("..")  # BAD! find a work around to import without installing
from stylechecker import (
    NodeType,
    TexTree,
    check_localization,
    check_acronyms,
    check_hyphenations,
)


class TestTexTree(unittest.TestCase):
    """Test case for TexTree class."""

    def setUp(self) -> None:
        """Increase the size of strings we can compare."""
        self.maxDiff = 2048

    def test_valid_latex(self) -> None:
        """Ensure that a valid LaTeX document can be parsed and that iteration
        is successful."""
        ground_truth = [
            {
                "type": NodeType.COMMAND,
                "content": "\\documentclass",
                "lineno": 1,
            },
            {
                "type": NodeType.TEXT,
                "content": "article",
                "lineno": 1,
            },
            {
                "type": NodeType.COMMAND,
                "content": "\\usepackage",
                "lineno": 2,
            },
            {
                "type": NodeType.TEXT,
                "content": "stylechecker",
                "lineno": 2,
            },
            {
                "type": NodeType.COMMAND,
                "content": "\\begin",
                "lineno": 3,
            },
            {
                "type": NodeType.TEXT,
                "content": "document",
                "lineno": 3,
            },
            {
                "type": NodeType.COMMENT,
                "content": "This line contains a comment",
                "lineno": 4,
            },
            {
                "type": NodeType.TEXT,
                "content": "This line contains text.",
                "lineno": 5,
            },
            {
                "type": NodeType.COMMAND,
                "content": "\\command[arg1][arg2]",
                "lineno": 6,
            },
            {
                "type": NodeType.TEXT,
                "content": "This line contains a command with arguments.",
                "lineno": 6,
            },
            {
                "type": NodeType.COMMAND,
                "content": "\\textit",
                "lineno": 7,
            },
            {
                "type": NodeType.TEXT,
                "content": "This line contains",
                "lineno": 7,
            },
            {
                "type": NodeType.COMMAND,
                "content": "\\textbf",
                "lineno": 7,
            },
            {
                "type": NodeType.TEXT,
                "content": "nested",
                "lineno": 7,
            },
            {
                "type": NodeType.TEXT,
                "content": "arguments.",
                "lineno": 7,
            },
            {
                "type": NodeType.COMMAND,
                "content": "\\checkhyphenation",
                "lineno": 8,
            },
            {
                "type": NodeType.COMMAND,
                "content": "\\end",
                "lineno": 9,
            },
            {
                "type": NodeType.TEXT,
                "content": "document",
                "lineno": 9,
            },
        ]
        with open(os.path.join("test", "test_valid.tex"), "r") as fp:
            tree = TexTree(fp.read())
        tree2list = list(tree)
        self.assertEqual(len(ground_truth), len(tree2list))
        for node, gt_vals in zip(tree2list, ground_truth):
            self.assertEqual(gt_vals["content"], node.content)
            self.assertEqual(gt_vals["type"], node.type)
            self.assertEqual(gt_vals["lineno"], node.lineno)

    def test_tostring(self) -> None:
        """Check that the tree class's __str__() method is functioning
        properly."""
        ground_truth = (
            "├── NodeType.COMMAND (1): \\documentclass\n"
            "│   └── NodeType.TEXT (1): article\n"
            "├── NodeType.COMMAND (2): \\usepackage\n"
            "│   └── NodeType.TEXT (2): stylechecker\n"
            "├── NodeType.COMMAND (3): \\begin\n"
            "│   └── NodeType.TEXT (3): document\n"
            "├── NodeType.COMMENT (4): This line contains a comment\n"
            "├── NodeType.TEXT (5): This line contains text.\n"
            "├── NodeType.COMMAND (6): \\command[arg1][arg2]\n"
            "│   └── NodeType.TEXT (6): This line contains a command with arguments.\n"
            "├── NodeType.COMMAND (7): \\textit\n"
            "│   ├── NodeType.TEXT (7): This line contains\n"
            "│   ├── NodeType.COMMAND (7): \\textbf\n"
            "│   │   └── NodeType.TEXT (7): nested\n"
            "│   └── NodeType.TEXT (7): arguments.\n"
            "├── NodeType.COMMAND (8): \\checkhyphenation\n"
            "└── NodeType.COMMAND (9): \\end\n"
            "    └── NodeType.TEXT (9): document\n"
        )
        with open(os.path.join("test", "test_valid.tex"), "r") as fp:
            tree = TexTree(fp.read())
            self.assertEqual(ground_truth, str(tree))


class TestCheckHyphenations(unittest.TestCase):
    """Test case for the hyphenation checking function."""

    def setUp(self) -> None:
        """Increase the size of strings we can compare."""
        self.maxDiff = 2048

    def tearDown(self) -> None:
        """Delete temporary files after each test."""
        try:
            os.remove("hyphenations.list")
            os.remove("hyphenations.warnings")
        except FileNotFoundError:
            pass

    def test_smoke(self) -> None:
        """Smoke test of check_hyphenation.  Passing this is the bare minimum
        required."""
        list_gt = (
            "Hyphenated words appearing in this document:\n"
            "fox-in appears 1 time\n"
            "in-socks appears 1 time\n"
            "fox-in-socks appears 2 times\n"
            "fox-in~socks appears 1 time\n"
            "fox~in-socks appears 1 time"
        )
        warnings_gt = (
            '"fox-in" also appears as "fox in" in test/test_hyphena'
            'tion.tex on line 4, "fox in" in test/test_hyphenation.'
            'tex on line 4, "fox~in" in test/test_hyphenation.tex o'
            'n line 5, "fox in" in test/test_hyphenation.tex on lin'
            'e 5, "fox~in" in test/test_hyphenation.tex on line 5, '
            '"fox~in" in test/test_hyphenation.tex on line 6\n'
            '"in-socks" also appears as "in socks" in test/test_hyp'
            'henation.tex on line 4, "in socks" in test/test_hyphen'
            'ation.tex on line 4, "in socks" in test/test_hyphenati'
            'on.tex on line 5, "in~socks" in test/test_hyphenation.'
            'tex on line 5, "in~socks" in test/test_hyphenation.tex'
            ' on line 5, "in~socks" in test/test_hyphenation.tex on'
            " line 6\n"
            '"fox-in-socks" also appears as "fox in socks" in test/'
            'test_hyphenation.tex on line 4, "foxinsocks" in test/t'
            'est_hyphenation.tex on line 4, "fox~in socks" in test/'
            'test_hyphenation.tex on line 5, "fox in~socks" in test'
            '/test_hyphenation.tex on line 5, "fox~in~socks" in tes'
            "t/test_hyphenation.tex on line 5\n"
            '"fox-in~socks" also appears as "fox in~socks" in test/'
            'test_hyphenation.tex on line 5, "fox~in~socks" in test'
            "/test_hyphenation.tex on line 5\n"
            '"fox~in-socks" also appears as "fox~in socks" in test/'
            'test_hyphenation.tex on line 5, "fox~in~socks" in test'
            "/test_hyphenation.tex on line 5"
        )
        check_hyphenations([os.path.join("test", "test_hyphenation.tex")])
        with open("hyphenations.list", "r") as list_f:
            self.assertEqual(list_gt, list_f.read())
        with open("hyphenations.warnings", "r") as warning_f:
            self.assertEqual(warnings_gt, warning_f.read())

    def test_multifile(self) -> None:
        """Test hyphentation checker's behavior when searching multiple
        files."""
        list_gt = (
            "Hyphenated words appearing in this document:\n"
            "bricks-with-blocks appears 1 time"
        )
        warnings_gt = (
            '"bricks-with-blocks" also appears as "bricks with '
            'blocks" in test/test_hyphenation_mf1.tex on line 4'
        )
        check_hyphenations(
            [
                os.path.join("test", "test_hyphenation_mf1.tex"),
                os.path.join("test", "test_hyphenation_mf2.tex"),
            ]
        )
        with open("hyphenations.list", "r") as list_f:
            self.assertEqual(list_gt, list_f.read())
        with open("hyphenations.warnings", "r") as warning_f:
            self.assertEqual(warnings_gt, warning_f.read())

    def test_nowarnings(self) -> None:
        """Test the case when no hyphenation warnings are present."""
        list_gt = "Hyphenated words appearing in this document:"
        check_hyphenations([os.path.join("test", "test_hyphenation_nowarn.tex")])
        with open("hyphenations.list", "r") as list_f:
            self.assertEqual(list_gt, list_f.read())
        self.assertFalse(os.path.isfile("hyphenations.warnings"))


class TestCheckAcronyms(unittest.TestCase):
    """Test case for the acronym checking function."""

    def setUp(self) -> None:
        """Increase the size of strings we can compare."""
        self.maxDiff = 2048

    def tearDown(self) -> None:
        """Delete temporary files after each test."""
        try:
            os.remove("acronyms.list")
            os.remove("acronyms.warnings")
        except FileNotFoundError:
            pass

    def test_smoke(self) -> None:
        """Smoke test of check_acronyms.  Passing this is the bare minimum
        required."""
        list_gt = (
            "Acronyms appearing in this document:\n"
            "CPU: Central Processing Unit\n"
            "GPU: Graphical Processing Unit\n"
            "RAM: "
        )
        warnings_gt = "The acronym RAM is possibly undefined."
        check_acronyms([os.path.join("test", "test_acronyms.tex")])
        with open("acronyms.list", "r") as list_f:
            self.assertEqual(list_gt, list_f.read())
        with open("acronyms.warnings", "r") as warning_f:
            self.assertEqual(warnings_gt, warning_f.read())


class TestCheckLocalization(unittest.TestCase):
    """Test case for the localization checking function."""

    def setUp(self) -> None:
        """Increase the size of strings we can compare."""
        self.maxDiff = 2048

    def tearDown(self) -> None:
        """Delete temporary files after each test."""
        try:
            os.remove("localization.list")
            os.remove("localization.warnings")
        except FileNotFoundError:
            pass

    def test_localization_error(self) -> None:
        """Check that two spelling schemes in the same document throws an
        error."""
        list_gt = (
            "US spellings used in this document:\n"
            "In test/test_localization_error.tex, line 4 the "
            'spellings: "Analyze" appear\n'
            "UK spellings used in this document:\n"
            "In test/test_localization_error.tex, line 5 the "
            'spellings: "Analyse" appear'
        )
        warnings_gt = (
            "Both US and UK spellings are used in the same "
            "document, please check the full build logs for "
            "details."
        )
        check_localization([os.path.join("test", "test_localization_error.tex")])
        with open("localization.list", "r") as list_f:
            self.assertEqual(list_gt, list_f.read())
        with open("localization.warnings", "r") as warning_f:
            self.assertEqual(warnings_gt, warning_f.read())

    def test_localization_no_error(self) -> None:
        """Check that the count of localized spellings is correct when none
        are present in the document."""
        list_gt = (
            "US spellings used in this document: None\n"
            "UK spellings used in this document: None"
        )
        warnings_gt = ""
        check_localization([os.path.join("test", "test_localization_no_error.tex")])
        with open("localization.list", "r") as list_f:
            self.assertEqual(list_gt, list_f.read())
        with open("localization.warnings", "r") as warning_f:
            self.assertEqual(warnings_gt, warning_f.read())


if __name__ == "__main__":
    unittest.main()
