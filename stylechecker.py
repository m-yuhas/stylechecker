#!/usr/bin/env python
"""Main module for LaTeX stylechecker package.  Stylechecker calls this script
and responses results are printed to stdout."""


from typing import Dict, List, Optional, Tuple
import argparse
import dataclasses
import os
import re


Tokens = List[Tuple[str, int]]


@dataclasses.dataclass
class TexNode:
    """Representation of one node of a LaTeX file tree."""
    content: str
    type: str
    lineno: int
    parent: object = None
    prev: object = None
    next: object = None
    child: object = None
    visited: bool = False

    def __str__(self) -> str:
        """String representation of node for use when printing a tree of nodes."""
        if self.next:
            return f'├── {self.type} ({self.lineno}): ' + self.content.replace("\n", "")
        else:
            return f'└── {self.type} ({self.lineno}): ' + self.content.replace("\n", "")


@dataclasses.dataclass
class CommandNode(TexNode):
    """Representation of command node in LaTeX tree."""
    args: List[TexNode] = dataclasses.field(default_factory=list)
            

class TexTree(object):
    """Represent the contents of a LaTeX document as a tree.

    Args:
        tex - string of the LaTeX document being analyzed.
    """

    def __init__(self, tex: str) -> None:
        tokens = TexTree.tokenize(tex)
        tokens.reverse()
        tokens, root = TexTree.parse(tokens)
        assert len(tokens) <= 0, \
            "Sorry, I wasn't able to parse the LaTeX document, please " \
            "check for unmatched {, [, ], or }"
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
        s = ''.join(["│   " if x else "    " for x in depth]) + f'{node}\n'
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
        curr_token = ''
        line_no = 1
        for char in s:
            if char == '\n':
                if curr_token != '':
                    tokens.append((curr_token, line_no))
                tokens.append((char, line_no))
                curr_token = ''
                line_no += 1
            elif (
                (
                    char == '{'
                    or char == '}'
                    or char == '%'
                    or char == '\\'
                    or char == '['
                    or char == ']'
                ) and not (
                    len(curr_token) > 0
                    and curr_token[-1] == '\\')
            ):
                if curr_token != '':
                    tokens.append((curr_token, line_no))
                tokens.append((char, line_no))
                curr_token = ''
            else:
                curr_token += char
        return tokens

    @staticmethod
    def parse(tokens: Tokens) -> Tuple[Tokens, TexNode]:
        """Build self from a list of tokens.

        Args:
            tokens: list of tokens from a LaTeX document
        """
        root = TexNode('', 'root', 0)
        curr_node = root
        curr_content = ''
        curr_type = 'text'
        while len(tokens) != 0:
            tok = tokens.pop()
            if tok[0] == '%' and curr_type != 'comment':
                next_node = TexNode(curr_content, curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = ''
                curr_type = 'comment'
            elif tok[0] == '\n':
                next_node = TexNode(curr_content, curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = ''
                curr_type = 'text'
            elif tok[0] == '\\' and curr_type != 'comment':
                next_node = TexNode(curr_content, curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = '\\'
                curr_type = 'command'
            elif tok[0] == '{' and curr_type != 'comment':
                next_node = TexNode(curr_content, curr_type, tok[1])
                tokens, next_node.child = TexTree.parse(tokens)
                next_node.child.parent = next_node
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = ''
                curr_type = 'text'
            elif tok[0] == '}' and curr_type != 'comment':
                next_node = TexNode(curr_content, curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node 
                return tokens, root
            elif tok[0] == '[' and curr_type == 'command':
                next_node = CommandNode(curr_content, curr_type, tok[1])
                tokens, arg = TexTree.parse(tokens)
                next_node.args.append(arg)
                curr_node.next = next_node
                next_node.prev = curr_node
                curr_node = next_node
                curr_content = ''
                curr_type = 'text'
            elif tok[0] == ']' and curr_type == 'command':
                next_node = TexNode(curr_content, curr_type, tok[1])
                curr_node.next = next_node
                next_node.prev = curr_node
                return tokens, root
            else:
                curr_content += tok[0]
        next_node = TexNode(curr_content, curr_type, tok[1])
        curr_node.next = next_node
        next_node.prev = curr_node
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
        if node.content.strip() == '':
            if node.prev:
                node.prev.next = node.next
                node = node.next
            elif node.parent and node.next:
                node.next.parent = node.parent
                node = node.next
            else:
                node = node.next
        return node


def check_localization(text: str) -> None:
    pass


def check_acronyms(text: str) -> None:
    """Find all acronyms used in the document text.  Write a list of acronyms and their definitions to 'acronyms.list' and write warning messages for acronyms missing definitions to 'acryonyms.warnings'.
    """
    pass


def check_hyphenations(docs: List[str]) -> None:
    """Find discrepancies in hyphenation of compound words, write a detailed
    report to 'compoundwords.list' and suspected discrepancies to
    'compoundwords.warnings'.
    
    Args:
        docs: a list of files comprising the project.
    """
    compound_words = {}
    for doc in docs:
        with open(doc, 'r') as fp:
            tree = TexTree(fp.read())
            for node in tree:
                if node.type == 'text':
                    matches = re.findall(r'(?:\S+-\S+)', node.content)
                    for m in matches:
                        if m not in compound_words:
                            compound_words[m] = []
                        compound_words[m].append((doc, node.lineno))
    mismatches = {}                    
    for doc in docs:
        with open(doc, 'r') as fp:
            tree = TexTree(fp.read())
            for node in tree:
                if node.type == 'text':
                    for word in compound_words:
                        matches = re.findall(
                            f'{"[^-]?".join(word.split("-"))}',
                            node.content)
                        for m in matches:
                            if m not in mismatches:
                                mismatches[word] = []
                            mismatches[word].append((doc, node.lineno, m))
    with open('compoundwords.list', 'w') as fp:
        fp.write('Compound words appearing in this document:')
        for word, appearances in compound_words.items():
            fp.write(f'\n{word} appears {len(appearances)} times')
    if len(mismatches) == 0:
        return
    with open('compoundwords.warnings', 'w') as fp:
        for word, appearances in mismatches.items():
            locations = ", ".join(
                [f'"{a[2]}" in {a[0]} on line {a[1]}' for a in appearances])
            fp.write(f'"{word}" also appears as {locations}')

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Utility to check for common trivial errors in LaTeX papers.')
    parser.add_argument(
        '-f',
        '--files',
        nargs='+',
        default=[],
        help='Path(s) to LaTeX file(s) to check.  If ommited all files with '
            'the *.tex extension in the current directory and its children '
            'will be checked.')
    parser.add_argument(
        '--hyphenation',
        action='store_true',
        help='Check that hyphenated words are hyphenated consistently .')
    parser.add_argument(
        '--acronyms',
        action='store_true',
        help='Check that all acronyms are defined.')
    parser.add_argument(
        '--localization',
        action='store_true',
        help='Check that words with two or more acceptable spellings are '
             'consistent.')
    args = parser.parse_args()
    tex_files = []
    if len(args.files) <= 0:
        print('HERE')
        for root, _, files in os.walk('.'):
            for f in files:
                if f.endswith('.tex'):
                    tex_files.append(os.path.join(root, f))
    else:
        print('OR HERE?')
        tex_files = args.files
    if args.hyphenation:
        check_hyphenations(tex_files)
    if args.acronyms:
        check_acronyms(tex_files)
    if args.localization:
        check_localization(tex_files)
