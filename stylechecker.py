#!/usr/bin/env python
"""Main module for LaTeX stylechecker package.  Stylechecker calls this script and responses results are printed to stdout."""


from typing import Dict, List, Tuple
import os
import re



def tokenize_tex(tex: str) -> List[str]:
    """TODO: Right now this package is just parsing all text in the .tex files, but the right way to do this is tokenize so that control sequences do not screw up the figuring.""" 
    for char in tex:
        pass


def find_acronyms(text: str) -> None:
    """Find all acronyms used in the document text.  Write a list of acronyms and their definitions to 'acronyms.list' and write warning messages for acronyms missing definitions to 'acryonyms.warnings'.
    """
    pass


def find_hyphenations(docs: List[str]) -> None:
    """Find discrepancies in hyphenation of compound words, write a detailed report to 'compoundwords.list' and suspected discrepancies to 'compoundwords.warnings'.
    
    Args:
        docs: a list of files comprising the project.
    """
    compound_words = {}
    for doc in docs:
        with open(doc, 'r') as fp:
            lines = fp.readlines()
            for idx, line in enumerate(lines):
                matches = re.findall(r'(?:\S+-\S+)', line)
                for m in matches:
                    if m not in compound_words:
                        compound_words[m] = []
                    compound_words[m].append((doc, idx))

    mismatches = {}                    
    for doc in docs:
        with open(doc, 'r') as fp:
            lines = fp.readlines()
            for idx, line in enumerate(lines):
                for word in compound_words:
                    matches = re.findall(f'{"[^-]?".join(word.split("-"))}', line)
                    for m in matches:
                        if m not in mismatches:
                            mismatches[word] = []
                        mismatches[word].append((doc, idx, m))
    
    with open('compoundwords.list', 'w') as fp:
        fp.write('Compound words appearing in this document:')
        for word, appearances in compound_words.items():
            fp.write(f'\n{word} appears {len(appearances)} times')
    if len(mismatches) == 0:
        return
    with open('compoundwords.warnings', 'w') as fp:
        for word, appearances in mismatches.items():
            locations = ", ".join([f'"{a[2]}" in {a[0]} on line {a[1]}' for a in appearances])
            fp.write(f'"{word}" also appears as {locations}')

    
if __name__ == '__main__':
    for root, _, files in os.walk('.'):
        tex_files = []
        for f in files:
            if f.endswith('.tex'):
                tex_files.append(os.path.join(root, f))
    
        find_hyphenations(tex_files)
