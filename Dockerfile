FROM python:3.11-alpine@sha256:5d769f990397afbb2aca24b0655e404c0f2806d268f454b052e81e39d87abf42 AS pipenv
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

FROM mvdan/shfmt@sha256:b1d072960db639a03069c95e8172582a06d57ad9bdfadbc4e51224dd09f73bc3 AS shfmt
ENTRYPOINT [ "/bin/shfmt" ]
