FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:8752572967b81f039861b521f0988f8394f5ee165afdf2527d5bccb228c371bb
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
