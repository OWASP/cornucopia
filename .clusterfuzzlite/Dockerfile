FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:b644037f0c08a75c2ee9650b3ec4349deb685f393f16c542f2bb3e5d402ae0f2
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
