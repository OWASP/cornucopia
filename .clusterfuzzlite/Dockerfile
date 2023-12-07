FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:c70b56b3611937b6448b58df8749935ed4603abfd3cd4964eac76324d7ee3761
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
