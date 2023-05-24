FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:1e3354dff09b410fba6f96371a469a34a7f0dacb15b2bcc548d8db5beadca049
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
