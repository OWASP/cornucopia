FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:a7eb0875e2d7e96eb7baab4f6104b077dd8d5a9aabcde40c9251f8ad33de0e36
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
