FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:92522ca36d1f73ca61ebde3c67624c56d98ff5d4f2383d87ed80a59537c3bc82
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
