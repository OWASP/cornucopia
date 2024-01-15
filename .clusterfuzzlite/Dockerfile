FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:a27f283b5d7332b667e7c5e7f54f085e88bdf8aa9579e3fe37c630cbd310cf0b
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
