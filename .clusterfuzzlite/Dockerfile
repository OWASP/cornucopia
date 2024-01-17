FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:95bed996ec54b0a38087bbc48f7945b31fbe00548a7adf7d8f3b564566b2123e
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
