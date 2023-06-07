FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:41a80931335f38378fc633c9120ede42c4c5811e6d1c8bf2c6029c459a6b61e0
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
