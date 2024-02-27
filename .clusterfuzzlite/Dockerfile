FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:eb94a1294a2f9e99b247ce74f18be25facfc7d3ff4740e21b2f008d27deaa6e0
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
