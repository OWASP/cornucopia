FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:5d94ec7a98cec672a69ecaa29602cff2932074fa5ba7e0d5f8158b872a1cfbfb
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
