# For system integration tests, we will use the official ShareLaTeX image.
# FROM docker.io/sharelatex/sharelatex-base:latest
FROM docker.io/library/ubuntu:20.04

# Install required TeX packages.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y texlive texlive-xetex

# Install Pip packages required to execute unit tests.
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install coverage black
#RUN pip install black coverage

# Set project folder as working directory; launch with Bash shell as default action.
VOLUME /stylechecker
WORKDIR /stylechecker
CMD /bin/bash

# Remember to bump version when 
LABEL version="0.0.4"
LABEL description="System integration test container for LaTeX stylechecker package."