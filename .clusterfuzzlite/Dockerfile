FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:d70626b61fdf678ddc1f6ba7f9366d33b6e28e823a6eeaaa1c19a37c5f27d4f4
RUN apt-get update && apt-get install -y make autoconf automake libtool curl gcc libc-dev software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt upgrade -y && apt-get install -y python3.10 python3.10-dev python3.10-distutils 
RUN apt-get install -y python3-pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN python3.10 -m pip install --upgrade setuptools setuptools_scm PyInstaller==6.6.0  #   meson ninja numpy pybind11 cython pythran
COPY . $SRC/cornucopia
WORKDIR $SRC/cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
