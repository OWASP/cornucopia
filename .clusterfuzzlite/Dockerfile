FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:46e1afeae454fe94f60a76a59c06ac1d37776aaf9373ac55a9fa6cfec917896b
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
