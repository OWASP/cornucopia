FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:89da609dc055ed2f4f713474a8d412781e91c5344f994f4f8b5098ca4621f258
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
