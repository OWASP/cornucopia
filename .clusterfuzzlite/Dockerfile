FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:746f59716717535e1b126113887a592581f46ab08081cf4ba799be2f41ef63bc
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
