FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:81b3668f504f6706f136cf5e3135385c479cead005f660f8ac285679157d3c40
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
