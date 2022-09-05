# For system integration tests, we will use the official ShareLaTeX image.
FROM docker.io/sharelatex/sharelatex-base:latest

# Install Pip packages required to execute unit tests.
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install coverage black

# Create a working directory and add our unit and integration tests.
RUN mkdir /stylechecker
RUN mkdir /stylechecker/test/
RUN mkdir /stylechecker/ci/
COPY stylechecker.py /stylechecker/
COPY stylechecker.sty /stylechecker/
COPY test/*.py /stylechecker/test/
COPY test/*.tex /stylechecker/test/
COPY ci/integration_test.py /stylechecker/ci/

# Launch with Bash shell as default action.
CMD /bin/bash

# Remember to bump version when 
LABEL version="0.0.1"
LABEL description="System integration test container for LaTeX stylechecker package."