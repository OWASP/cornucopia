FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:3194cc23683b71b730b36ded3e75ceb10a6955e386394cfe091a698701f7c6ca
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
