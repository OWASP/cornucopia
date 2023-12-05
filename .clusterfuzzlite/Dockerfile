FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:e2e4108094972e88ff309f9c8942bc840d437b52dbb3095c1bf2a9491a1d11f2
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
