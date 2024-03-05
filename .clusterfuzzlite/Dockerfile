FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:973f3ae35d69301eb5063382b3b2a37c06e2dc6725ef2493f3b023e322cdc329
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
