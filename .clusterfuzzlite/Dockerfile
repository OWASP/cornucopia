FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:fbead50f501f4c4629b4fa29e3a4cf839d1bdaf7bc161329114760c1f975cc82
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
