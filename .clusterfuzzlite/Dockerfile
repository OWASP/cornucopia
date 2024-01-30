FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:6296095280f2f06137a3710b1b204ec7dbdcbbf9861c37816a5d491177b39f04
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
