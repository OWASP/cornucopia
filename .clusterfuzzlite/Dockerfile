FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:5fa0d885e12eac50d065ad4c060425ef969429161242e18d71d7fa2f5a220c08
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
