FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:3434621b4da345fffd8d4b1342f3b6d8ad1b5510cdd8830b4bc4419d20b5855f
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
