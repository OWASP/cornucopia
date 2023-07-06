FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:72c7f06e314034989837c62ef459d9af25c147dcee0efae371a0b3e6e1fad0f5
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
