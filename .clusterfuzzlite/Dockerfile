FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:96a19a6c9f0a19507f255f647afcd12208ce8aad3d8bdf37b60a354857194271
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
