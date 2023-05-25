FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:08f8affbdd1b9fccf8c92ff06098fd45f5d8734b17061fe6f72d7d32815d57f1
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
