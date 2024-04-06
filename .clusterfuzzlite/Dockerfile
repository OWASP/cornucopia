FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:5273c1d371609208508533e75face1db03ec1bf7512ba4b895bfc7ef6d3cd7f7
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
