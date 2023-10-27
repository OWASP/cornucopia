FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:1a58cd33d342da78f9975fed4629466d0dd7155a5c87912d8f5bf3f6faf6f797
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/cornucopia
WORKDIR cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
