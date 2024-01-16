FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:28fe69f883e32eb0274d8c85f2c007e2d8186c1b9fb0f6a7f7aece472f9bc20d
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
