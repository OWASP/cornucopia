FROM python:3.12-alpine@sha256:a0c22d88d8a5738d8dbe0d4482783f6d39595182b02df694ca170c664afff2b7 AS pipenv
RUN apk add --no-cache shadow
# UID of current user who runs the build
ARG user_id
# GID of current user who runs the build
ARG group_id
# HOME of current user who runs the build
ARG home
# change GID for dialout group which collides with MacOS staff GID (20) and
# create group and user to match permmisions of current who runs the build
ARG workdir
WORKDIR ${workdir}
RUN groupmod -g 64 dialout \
    && addgroup -S -g "${group_id}" union \
    && groupmod -g 2999 ping \
    && mkdir -p "${home}" \
    && adduser -S -u "${user_id}" -h "${home}" -s "/bin/bash" -G union builder
# Add pip and build requirements
RUN apk add --no-cache \
    bash \
    curl \
    docker \
    gcc \
    git \
    libc-dev \
    make
COPY --chown=builder:union requirements.txt ./
RUN pip install -r requirements.txt --require-hashes
USER builder
# Install Python dependencies so they are cached
ARG workdir
WORKDIR ${workdir}
COPY --chown=builder:union Pipfile Pipfile.lock ./
RUN pipenv --python `which python` install --ignore-pipfile --dev
ENTRYPOINT [ "/usr/local/bin/pipenv" ]

FROM mvdan/shfmt@sha256:a767cff74d40e3d2085020640a6d0200f1588e6201c6c04e5e7ff6fa681bccd9 AS shfmt
ENTRYPOINT [ "/bin/shfmt" ]
