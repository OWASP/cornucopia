FROM gcr.io/oss-fuzz-base/base-builder-python:v1@sha256:5273c1d371609208508533e75face1db03ec1bf7512ba4b895bfc7ef6d3cd7f7
RUN apt-get update && apt-get install -y make autoconf automake libtool curl gcc libc-dev software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt upgrade && apt-get install -y python3.10 python3.10-dev python3.10-distutils 
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 4
RUN update-alternatives --set python3 /usr/bin/python3.10
RUN apt-get install -y python3-pip
RUN python3 -m pip install --upgrade pip
COPY . $SRC/cornucopia
WORKDIR $SRC/cornucopia
COPY .clusterfuzzlite/build.sh $SRC/
