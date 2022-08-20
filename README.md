# Style Checker

## Introduction
Tired of writing papers and hyphenating specialized vocabulary diffently everytime you type?  Not sure if you defined that acronym in the text already or not?  This LaTeX package generates warning messages when any of these issues occur, so you can write more consistently.

## Quick Start
This package has only been tested on Overleaf with the pdflatex compiler.  Perhaps other platforms will be supported in the future, but for now your mileage may vary.

1. Upload the ```stylechecker.py``` and ```stylechecker.sty``` files from this repo to the root directory of your Overleaf project.
2. Include this package in your main .tex file: ```\usepackage{stylechecker}```
3. Add the command ```\checkhyphenation{}``` somewhere in your document to check for inconsistant hyphenation.  If some instances are found, a warning message will appear at compile time.

## Contributing
If you find a bug or want an additional feature, please open an issue on the GitHub issue tracker.  If you fix a bug yourself or want to contribute a new feature, please feel free to make a pull request.
