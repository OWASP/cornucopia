FROM gcr.io/oss-fuzz-base/base-builder-python:ubuntu-24-04@sha256:79f6e0ac4506a75757099bfea8cfd52d1bb0e2f92ca21c64755151b655ce23e1

# System dependencies + Python tooling
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

# Try to add deadsnakes and install Python 3.13, but don't fail if packages are missing
RUN set -eux; \
    add-apt-repository ppa:deadsnakes/ppa -y; \
    apt-get update; \
    if ! apt-get install -y --no-install-recommends \
        python3.13 \
        python3.13-dev \
        python3.13-distutils \
        python3.13-venv \
        python3.13-pip; then \
      echo 'python3.13 packages not available, continuing with existing python3'; \
    fi; \
    rm -rf /var/lib/apt/lists/*

# Ensure pip + tools; prefer python3.13 if it exists, otherwise use existing python3
RUN if command -v python3.13 >/dev/null 2>&1; then \
      curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13 && \
      python3.13 -m pip install --no-cache-dir --upgrade \
        PyInstaller==6.18.0 \
        setuptools \
        setuptools_scm \
        wheel; \
    else \
      curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
      python3 -m pip install --no-cache-dir --upgrade \
        PyInstaller==6.18.0 \
        setuptools \
        setuptools_scm \
        wheel; \
    fi

# Atheris only supports python 3.11
# https://github.com/google/atheris/blob/master/README.md#installation-instructions
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY . $SRC/cornucopia
WORKDIR $SRC/cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
