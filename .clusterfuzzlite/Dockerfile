FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:5738485a1636fe5d72047753b6b7d959790c62a865f0a16c165e1c9d175ec953
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
