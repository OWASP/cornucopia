FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:fb74bd185059ef12847665846c9f665d6fe8947db658bcc4aa99bce582b0c834
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
