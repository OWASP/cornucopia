FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:fcd754029096671fa4a0ec3eb2a089ccd86f0d1e81d7d4420170b50701681023
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
