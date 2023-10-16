FROM python:3.11-alpine@sha256:cd311c6a0164f34a7edbf364e05258b07d66d3f7bc155139dcb9bef88a186ded AS pipenv
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

FROM mvdan/shfmt@sha256:8b4a7a6e1246a922bde122a6343c68e96bad336cd69dbcc4963fc965d1893bb6 AS shfmt
ENTRYPOINT [ "/bin/shfmt" ]
