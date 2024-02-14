FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:4b45d0910d6ce4e229ab8fe4b0d4d7ccabd17d4f509552fda5cc682c1cd4acbe
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
