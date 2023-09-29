FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:d92a7566dc75976cde6f50835f0a196f9fa5201a9b1c9c7a214f6d30fda86597
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
