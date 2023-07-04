FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:3d08b840c0b7abc211cdd72292beaf3358bb7c879d869645a41117b48372ae66
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
