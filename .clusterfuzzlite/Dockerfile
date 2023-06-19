FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:d3764429edd157258759f49596f62025f10015ee99bad1b02a654c355954bc8b
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
