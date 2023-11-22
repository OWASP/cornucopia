FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:ccd0e4c89a6b945d697308f5317ec5eb5a7965359d2851182151f8957af27ba0
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
