FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:3d7dc6e9f8dbfa89c5a03d5a5d83c52240fb08f080633da210cae1b71638a67d
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
