FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:fd3bd57c3f12a8f8010c1e874f20c9aff339c5e0c75669b3b4f2988e0c998ce9
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
