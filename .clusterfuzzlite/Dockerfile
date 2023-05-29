FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:620538266a773b48010eca2d0b656c54b21d054637e7e7c14de6c67e577c9b1a
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
