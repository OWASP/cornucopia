FROM gcr.io/oss-fuzz-base/base-builder-python:ubuntu-24-04@sha256:79f6e0ac4506a75757099bfea8cfd52d1bb0e2f92ca21c64755151b655ce23e1
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    build-essential \
    zlib1g-dev \
    libssl-dev \
    libffi-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -O https://www.python.org/ftp/python/3.13.1/Python-3.13.1.tgz \
    && tar -xzf Python-3.13.1.tgz \
    && cd Python-3.13.1 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. && rm -rf Python-3.13.1 Python-3.13.1.tgz
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13
RUN python3.13 -m pip install --no-cache-dir --upgrade PyInstaller==6.18.0 setuptools setuptools_scm wheel
COPY . $SRC/cornucopia
WORKDIR $SRC/cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
