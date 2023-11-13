FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:d07bcc06245f85d571459c21af928b62f41eb6476cc92b1738745db906dc61fc
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
