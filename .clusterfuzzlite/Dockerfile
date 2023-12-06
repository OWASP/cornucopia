FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:3a639d55d8f24585a8eceee010b9a52632e215fd09ad02981030b1cb5894cb24
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
