FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:bd7a4d2fc4d9cc70cf11789bd0feaf0a09c9a4e2e5e44184d4a4a731e4bc617d
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
