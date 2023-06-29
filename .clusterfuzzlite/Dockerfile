FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:c62a05a2f4fc7118cc52b50ac526210237993496aeb3910af69a5e5bc960b160
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
