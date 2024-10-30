FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:437ef4d9f60c4eb6d8f0d941a2babcaf990bcf778647179e6eb31fb599c265fb
RUN apt-get update && apt-get install -y make autoconf automake libtool curl gcc libc-dev software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
# Atheris only supports python 3.11 https://github.com/google/atheris/blob/master/README.md#installation-instructions
RUN apt upgrade -y && apt-get install -y python3.10 python3.10-dev python3.10-distutils libxml2-dev  libxslt-dev
RUN apt-get install -y python3-pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN python3.10 -m pip install --upgrade setuptools setuptools_scm PyInstaller==6.11.0
COPY . $SRC/cornucopia
WORKDIR $SRC/cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
