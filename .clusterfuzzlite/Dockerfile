FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:e38c4048901dbb30c3e11e3426e09abb5809ad781ad21dac617b9d175eec79a8
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
