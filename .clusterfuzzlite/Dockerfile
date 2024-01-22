FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:1c6ae6cee22206e1526050a02ed68cffd7d299a155986d5bbdb2e9f72264187f
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
