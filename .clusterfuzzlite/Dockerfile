FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:93f994e4219175bdf2034737170c89f4309b44480a182194382284fd122f5404
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
