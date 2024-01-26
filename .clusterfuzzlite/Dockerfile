FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:05f5dc2f4f70b72f5d5bf18fedf78d1c6f81980cf0c489782b0de361326685b2
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
