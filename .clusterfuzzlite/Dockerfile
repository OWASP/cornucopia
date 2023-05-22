FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:05c5210560eff674d7d620ce71b78dbb0b2b99729656335fe7ddd231d673169c
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
