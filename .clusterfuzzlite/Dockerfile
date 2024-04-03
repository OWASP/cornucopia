FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:ca45ddab154bc19d45352537133735a771381afffa06526c4b5fe76df029582b
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
