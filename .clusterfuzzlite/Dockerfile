FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:038879f46b2fc4f6dfe755c5908ddcd831febe30c61e868c64145bc14aa66929
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
