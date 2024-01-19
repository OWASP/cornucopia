FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:53e63d615304f9384933dfae2ca2ec9d442d13ff26c1561ec9dda5318e10bb56
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
