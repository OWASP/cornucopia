FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:c030cd8381f6db00d004f295580b7a72b0d4301cd0ccfa8e3597658394ee1b4f
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
