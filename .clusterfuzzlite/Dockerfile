FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:f08928808ba3261311bf1cc62e5c7ccec0a1a6c0a5bdb03e2c0ef3cf2d2b4af9
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
