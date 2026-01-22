FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:c0021e88f13312e7706c49e6348fe442b641ff46d032d9846131a60b68dea50d
RUN apt-get update && apt-get install -y --no-install-recommends autoconf automake curl gcc libc-dev libtool make software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
# Atheris only supports python 3.11 https://github.com/google/atheris/blob/master/README.md#installation-instructions
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    libxml2-dev \
    libxslt-dev \
    python3.10 \
    python3.10-dev \
    python3.10-venv
RUN apt-get clean
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN python3.10 -m pip install --upgrade wheel setuptools setuptools_scm PyInstaller==6.13.0
COPY . $SRC/cornucopia
WORKDIR $SRC/cornucopia
COPY .clusterfuzzlite/build.sh $SRC/