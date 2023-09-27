FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:e462cd28f361287ebe9e305b84a57cdd20e28bcbe8cdb29028c5235e03608ae5
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
