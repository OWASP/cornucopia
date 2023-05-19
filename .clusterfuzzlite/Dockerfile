FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:c52f920f4c057e04114972891af85c3cb8c9806e4bf7fd8fea6d4f42514573ca
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
