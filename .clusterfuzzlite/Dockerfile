FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:57a6a387e7e2fd50e6f7221141c8ade99a7c0e027d6786b5aeaf4196eec8cb7a
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
