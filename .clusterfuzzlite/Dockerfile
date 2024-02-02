FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:8ce4fb1dfb2be485c9c738368bb3a516eea71642a293d53e1c4550347e2bcb1b
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
