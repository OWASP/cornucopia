FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:bdc7386b959530e3a7e508097ff264455ef378d4fd6c51dd137661314478998a
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
