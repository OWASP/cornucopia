FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:c8887d994325639254296044331492c8fbf53dac6aa035b53a8134535668ac22
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
