FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:5052483b8bf39ae544e40eb7b7ec1ea7c5fed5b0279bd3d4f415be4519d54690
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
