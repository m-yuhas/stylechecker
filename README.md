# Style Checker (for LaTeX)

## Introduction
Tired of writing papers and accindentally hyphenating specialized vocabulary diffently everytime you type?  Not sure if you defined that acronym in the text already or not?  This LaTeX package generates warning messages when any of these issues occur, so you can write more consistently.

## Quick Start
This package has only been tested on Overleaf with the pdflatex and xelatex compilers.  Perhaps other platforms will be supported in the future, but for now your mileage may vary.

1. Upload the ```stylechecker.py``` and ```stylechecker.sty``` files from this repo to the root directory of your Overleaf project.
2. Include this package in your main .tex file: ```\usepackage{stylechecker}```
3. Add the command ```\checkhyphenation{}``` somewhere in your document to check for inconsistant hyphenation (e.g., "hyper-parameters" and "hyperparameters").  If some instances are found, a warning message will appear at compile time.
4. Add the command ```\checkacronyms{}``` somewhere in your document to generate a list of all acronyms used and their definitions.  If an acronym wasn't defined, a warning message will be displayed.
5. Add the command ```\checklocalization{}``` to check if both US and UK spellings appear in the same document.  If both are present, the build log will point you to each instance, so you know what to change.


## Contributing
If you find a bug or want an additional feature, please open an issue on the GitHub issue tracker.  If you fix a bug yourself or want to contribute a new feature, please feel free to make a pull request.

A [Dockerfile](https://docs.docker.com/get-docker/) is provided to establish a consistant test environment across platforms. To build the docker image run the following from this repository's root directory:

```
docker build . --file ci/Dockerfile --tag stylechecker:latest
```

It is recommended to use [Black](https://github.com/psf/black) to format any Python files:

```
docker run -v $PWD:/stylechecker stylechecker:latest black --check /stylechecker/
```

Finally, unit tests are provided to test individual functions in ```stylechecker.py``` while integration tests are provided to test the end-to-end functionality with the LaTeX compiler in-loop.  To run the unit tests:

```
docker run -v $PWD:/stylechecker stylechecker:latest coverage run -m unittest test.test_stylechecker
```

To run the integration tests:

```
docker run -v $PWD:/stylechecker stylechecker:latest python3 -m unittest ci.integration_test
```

## Documentation in Other Languages
[Documentación en español](doc/L%C3%89AME.md)

[Documentation en français](doc/LISEZ-MOI.md)

[Documentazione in italiano](doc/LEGGIMI.md)

[中文手冊](doc/%E8%AE%80%E6%88%91%E6%AA%94%E6%A1%88.md)