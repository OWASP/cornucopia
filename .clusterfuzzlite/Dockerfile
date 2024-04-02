FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:600ed64bd9aeab3ab1e688003bee82ff9dd7db19477f77836d381049882e1061
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
