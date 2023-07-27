FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:c03746cb30fcfc09b1b16c8c72b2d0a632f143dade36beebfa692e983c3d05b8
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
