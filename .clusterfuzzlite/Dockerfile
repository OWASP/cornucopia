FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:1e35dcf0ab8b5b09259e88cad2a814b356f0fdab0a8fb0bfdef24f3837a4337f
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
