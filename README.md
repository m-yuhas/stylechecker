# Style Checker

## Introduction
Tired of writing papers and hyphenating specialized vocabulary diffently everytime you type?  Not sure if you defined that acronym in the text already or not?  This LaTeX package generates warning messages when any of these issues occur, so you can write more consistently.

## Quick Start
This package has only been tested on Overleaf with the pdflatex compiler.  Perhaps other platforms will be supported in the future, but for now your mileage may vary.

1. Upload the ```stylechecker.py``` and ```stylechecker.sty``` files from this repo to the root directory of your Overleaf project.
2. Include this package in your main .tex file: ```\usepackage{stylechecker}```
3. Add the command ```\checkhyphenation{}``` somewhere in your document to check for inconsistant hyphenation.  If some instances are found, a warning message will appear at compile time.

## Future Tasks
1. Tokenize the .tex files to avoid checking comments and achieve consistent behaviour inside commands
2. Add acronym finder
3. Check for camel case inconsitencies
4. Add ignore command to override
5. Support lualatex and xelatex compilers
