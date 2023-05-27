FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:1cf2794dd74cd067478e17e348b70b63cc40fa199b8c39e613bb32a64cc37945
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
