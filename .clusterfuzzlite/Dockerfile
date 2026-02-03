FROM gcr.io/oss-fuzz-base/base-builder-python:ubuntu-24-04@sha256:79f6e0ac4506a75757099bfea8cfd52d1bb0e2f92ca21c64755151b655ce23e1

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    autoconf \
    automake \
    curl \
    gcc \
    libc-dev \
    libtool \
    make \
    libxml2-dev \
    libxslt-dev \
    python3-dev \
    python3-venv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python 3.13 and make it the default python3
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.13 \
        python3.13-venv \
        python3.13-dev && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/python3.13 /usr/local/bin/python3 && \
    ln -sf /usr/bin/python3.13 /usr/bin/python3 && \
    python3 --version

# Atheris only supports python 3.11
# https://github.com/google/atheris/blob/master/README.md#installation-instructions
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3
RUN python3 -m pip install --no-cache-dir --upgrade PyInstaller==6.18.0 setuptools setuptools_scm wheel

COPY . $SRC/cornucopia
WORKDIR $SRC/cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
