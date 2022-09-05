#!/usr/bin/env python
"""Main module for LaTeX stylechecker package.  Stylechecker calls this script
and responses results are printed to stdout."""


from typing import Dict, List, Optional, Tuple
import argparse
import dataclasses
import enum
import os
import re


Tokens = List[Tuple[str, int]]


class NodeType(enum.Enum):
    """Possible types that a node in a TexTree can take."""

    ROOT = 0
    COMMENT = 1
    COMMAND = 2
    TEXT = 3


@dataclasses.dataclass
class TexNode:
    """Representation of one node of a LaTeX file tree.

    Args:
        contents - the text contained within a node.
        type - whether the node is a command, text, or comment.
        lineno - line number in the .tex file where this node occurs.
        parent - pointer to this node's parent (if any).
        prev - pointer the previous node in the tree (if any).
        next - pointer to the next node in the tree (if any).
        child - pointer to this node's child (if any).
        visited - used during iteration, True if this node has already been
            visited.
    """

    content: str
    type: NodeType
    lineno: int
    parent: object = None
    prev: object = None
    next: object = None
    child: object = None
    visited: bool = False

    def __str__(self) -> str:
        """String representation of node for use when printing a tree of nodes."""
        if self.next:
            return f"├── {self.type} ({self.lineno}): " + self.content.replace("\n", "")
        else:
            return f"└── {self.type} ({self.lineno}): " + self.content.replace("\n", "")


class TexTree(object):
    """Represent the contents of a LaTeX document as a tree.  In this tree
    each node's child represents an element contained within it.  For
    instance, in '\textbf{Hello World!}', '\textbf' is a command and
    'Hello World!' is its child.  Each node can only have one child.
    Successive nodes (e.g., new paragraphs) are represented as a doubly
    linked-list at each child.  Elements of this linked-list can also contain
    their own children.

    Args:
        tex - string of the LaTeX document being analyzed.
    """

    def __init__(self, tex: str) -> None:
        tokens = TexTree.tokenize(tex)
        tokens.reverse()
        tokens, root = TexTree.parse(tokens)
        assert len(tokens) <= 0, (
            "Sorry, I wasn't able to parse the LaTeX document, please "
            "check for unmatched {, [, ], or }"
        )
        self.root = TexTree.prune(root)

    def __str__(self) -> str:
        """Print the tree like the Unix tree command."""
        return TexTree.tostring(self.root, [])

    def __iter__(self) -> None:
        """Return an iterator for the TexTree."""
        self.node = self.root
        return self

    def __next__(self) -> TexNode:
        """Return the next TexNode when iterating through the tree depth
        first."""
        if not self.node.visited:
            self.node.visited = True
            return self.node
        if self.node.child:
            self.node = self.node.child
            self.node.visited = True
            return self.node
        if self.node.next:
            self.node = self.node.next
            self.node.visited = True
            return self.node
        while self.node.prev:
            self.node = self.node.prev
        while self.node.parent:
            self.node = self.node.parent
            if self.node.next:
                self.node = self.node.next
                self.node.visited = True
                return self.node
        raise StopIteration

    @staticmethod
    def tostring(node: TexNode, depth: List[bool]) -> str:
        """Print an individual node of the tree in its place in the larger
        tree."""
        s = "".join(["│   " if x else "    " for x in depth]) + f"{node}\n"
        if node.child:
            depth.append(True if node.next else False)
            s += TexTree.tostring(node.child, depth)
            depth.pop()
        if node.next:
            s += TexTree.tostring(node.next, depth)
        return s

    @staticmethod
    def tokenize(s: str) -> Tokens:
        """Tokenize a LaTeX document.

        Args:
            s: stringified contents of document

        Returns:
            A list of tokens.  Each token is a tuple consisting of a string
            (the token itself), and its associated line number.
        """
        tokens = []
        curr_token = ""
        line_no = 1
        for char in s:
            if char == "\n":
                if curr_token != "":
                    tokens.append((curr_token, line_no))
                tokens.append((char, line_no))
                curr_token = ""
                line_no += 1
            elif (char == "{" or char == "}" or char == "%" or char == "\\") and not (
                len(curr_token) > 0 and curr_token[-1] == "\\"
            ):
                if curr_token != "":
                    tokens.append((curr_token, line_no))
                tokens.append((char, line_no))
                curr_token = ""
            else:
                curr_token += char
        return tokens

    @staticmethod
    def parse(tokens: Tokens) -> Tuple[Tokens, TexNode]:
        """Build self from a list of tokens.

        Note 1: currently arguments to command in [] are ignored and treated
        as text.

        Note 2: if the LaTeX is invalid (e.g., extra or missing { or }), the
        parser will still return its best attempt at forming a tree.  This
        should not be used to check the validity of LaTeX syntax.

        Args:
            tokens: list of tokens from a LaTeX document
        """
        root = TexNode("", NodeType.ROOT, 0)
        curr_node = root
        curr_content = ""
        curr_type = NodeType.TEXT
        while len(tokens) != 0:
            tok = tokens.pop()
            if tok[0] == "%" and curr_type != NodeType.COMMENT:
                next_node = TexNode(curr_content.strip(), curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = ""
                curr_type = NodeType.COMMENT
            elif tok[0] == "\n":
                next_node = TexNode(curr_content.strip(), curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = ""
                curr_type = NodeType.TEXT
            elif tok[0] == "\\" and curr_type != NodeType.COMMENT:
                next_node = TexNode(curr_content.strip(), curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = "\\"
                curr_type = NodeType.COMMAND
            elif tok[0] == "{" and curr_type != NodeType.COMMENT:
                next_node = TexNode(curr_content.strip(), curr_type, tok[1])
                tokens, next_node.child = TexTree.parse(tokens)
                next_node.child.parent = next_node
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = ""
                curr_type = NodeType.TEXT
            elif tok[0] == "}" and curr_type != NodeType.COMMENT:
                next_node = TexNode(curr_content.strip(), curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node
                return tokens, root
            else:
                curr_content += tok[0]
        return tokens, root

    @staticmethod
    def prune(node: TexNode) -> TexNode:
        """Prune empty nodes from a Tex document tree.

        Args:
            node - root of the TexTree.

        Returns:
            The new root node of the TexTree.
        """
        if node.next:
            node.next = TexTree.prune(node.next)
        if node.child:
            node.child = TexTree.prune(node.child)
        if node.content == "":
            if node.prev:
                node.prev.next = node.next
                node = node.next
            elif node.parent and node.next:
                node.next.parent = node.parent
                node = node.next
            else:
                node = node.next
        return node


def check_localization(docs: List[str]) -> None:
    """Find inconsitent use of localized spellings (e.g. analysed and
    analyzed) in the same document.  Write a list of discrepancies to
    'loc.list' and write warning messages for the discrepancies to
    'loc.warnings'.

    Args:
        docs: a list of files comprising the project.
    """
    us_spellings = []
    uk_spellings = []
    for doc in docs:
        with open(doc, "r") as fp:
            tree = TexTree(fp.read())
            for node in tree:
                if node.type == NodeType.TEXT:
                    us_matches = re.findall(
                        r"(\w+zation|\w+yze|\w+yzing|\w+our|\w+our\w+|\w+re)\b",
                        node.content,
                    )
                    if len(us_matches) > 0:
                        us_spellings.append((us_matches, doc, node.lineno))
                    uk_matches = re.findall(
                        r"(\w+sation|\w+yse|\w+ysing|\w+our|\w+our\w+|\w+re)\b",
                        node.content,
                    )
                    if len(uk_matches) > 0:
                        uk_spellings.append((uk_matches, doc, node.lineno))
    with open("localization.list", "w") as list_f:
        list_f.write("US spellings used in this document:")
        for item in us_spellings:
            word_list = ", ".join([f'"{x}"' for x in item[0]])
            list_f.write(
                f"\nIn {item[1]}, line {item[2]} the spellings: " f"{word_list} appear"
            )
        if len(us_spellings) == 0:
            list_f.write(" None")
        list_f.write("\nUK spellings used in this document:")
        for item in uk_spellings:
            word_list = ", ".join([f'"{x}"' for x in item[0]])
            list_f.write(
                f"\nIn {item[1]}, line {item[2]} the spellings: " f"{word_list} appear"
            )
        if len(uk_spellings) == 0:
            list_f.write(" None")
    with open("localization.warnings", "w") as warn_f:
        if len(us_spellings) > 0 and len(uk_spellings) > 0:
            warn_f.write(
                "Both US and UK spellings are used in the same document, "
                "please check the full build logs for details."
            )


def check_acronyms(docs: List[str]) -> None:
    """Find all acronyms used in the document text.  Write a list of acronyms
    and their definitions to 'acronyms.list' and write warning messages for
    acronyms missing definitions to 'acryonyms.warnings'.

    Args:
        docs: a list of files comprising the project.
    """
    acronyms = {}
    for doc in docs:
        with open(doc, "r") as fp:
            tree = TexTree(fp.read())
            for node in tree:
                if node.type == NodeType.TEXT:
                    matches = re.findall(r"\b([A-Z]{2,})\b", node.content)
                    for m in matches:
                        if m not in acronyms:
                            acronyms[m] = []
                        before = (
                            "("
                            + "".join([c + "\\w+\\s" for c in m[:-1]])
                            + m[-1]
                            + "\\w+|"
                            + "".join([c.lower() + "\\w+\\s" for c in m[-1]])
                            + m[-1]
                            + "\\w+)\s+\\("
                            + m
                            + "\\)"
                        )
                        after = (
                            m
                            + "\s\\(("
                            + "".join([c + "\\w+\\s" for c in m[:-1]])
                            + m[-1]
                            + "\\w+|"
                            + "".join([c.lower() + "\\w+\\s" for c in m[:-1]])
                            + m[-1].lower()
                            + "\\w+)\\)"
                        )
                        acronyms[m].extend(re.findall(before, node.content))
                        acronyms[m].extend(re.findall(after, node.content))
    with open("acronyms.list", "w") as list_f:
        list_f.write("Acronyms appearing in this document:")
        for acronym, definitions in acronyms.items():
            list_f.write(f'\n{acronym}: {", ".join(definitions)}')
    with open("acronyms.warnings", "w") as warn_f:
        for acronym, definitions in acronyms.items():
            if len(definitions) == 0:
                warn_f.write(f"The acronym {acronym} is possibly undefined.\n")
        if warn_f.tell() - 1 > 0:
            warn_f.seek(warn_f.tell() - 1)
            warn_f.truncate()


def check_hyphenations(docs: List[str]) -> None:
    """Find discrepancies in hyphenation of compound words, write a detailed
    report to 'compoundwords.list' and suspected discrepancies to
    'compoundwords.warnings'.

    Args:
        docs: a list of files comprising the project.
    """
    trees = []
    compound_words = {}
    for doc in docs:
        with open(doc, "r") as fp:
            tree = TexTree(fp.read())
            for node in tree:
                if node.type == NodeType.TEXT:
                    matches = re.findall(r"\b(?:\S+-\S+)\b", node.content)
                    for m in matches:
                        if m not in compound_words:
                            compound_words[m] = []
                        compound_words[m].append((doc, node.lineno))
            trees.append((tree, doc))
    mismatches = {}
    for tree, doc in trees:
        for node in tree:
            if node.type == NodeType.TEXT:
                for word in compound_words:
                    matches = re.findall(
                        f'\\b{"[^-]?".join(re.split("[-]", word))}\\b', node.content
                    )
                    for m in matches:
                        if word not in mismatches:
                            mismatches[word] = []
                        mismatches[word].append((doc, node.lineno, m))
    with open("hyphenations.list", "w") as list_f:
        list_f.write("Hyphenated words appearing in this document:")
        for word, appearances in compound_words.items():
            list_f.write(
                f"\n{word} appears {len(appearances)} time"
                f'{"s" if len(appearances) != 1 else ""}'
            )
    if len(mismatches) == 0:
        return
    with open("hyphenations.warnings", "w+") as warn_f:
        for word, appearances in mismatches.items():
            locations = ", ".join(
                [f'"{a[2]}" in {a[0]} on line {a[1]}' for a in appearances]
            )
            warn_f.write(f'"{word}" also appears as {locations}\n')
        if warn_f.tell() - 1 > 0:
            warn_f.seek(warn_f.tell() - 1)
            warn_f.truncate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Utility to check for common trivial errors in LaTeX papers."
    )
    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        default=[],
        help="Path(s) to LaTeX file(s) to check.  If ommited all files with "
        "the *.tex extension in the current directory and its children "
        "will be checked.",
    )
    parser.add_argument(
        "--hyphenation",
        action="store_true",
        help="Check that hyphenated words are hyphenated consistently .",
    )
    parser.add_argument(
        "--acronyms", action="store_true", help="Check that all acronyms are defined."
    )
    parser.add_argument(
        "--localization",
        action="store_true",
        help="Check that words with two or more acceptable spellings are "
        "consistent.",
    )
    args = parser.parse_args()
    tex_files = []
    if len(args.files) <= 0:
        for root, _, files in os.walk("."):
            for f in files:
                if f.endswith(".tex"):
                    tex_files.append(os.path.join(root, f))
    else:
        tex_files = args.files
    if args.hyphenation:
        check_hyphenations(tex_files)
    if args.acronyms:
        check_acronyms(tex_files)
    if args.localization:
        check_localization(tex_files)
