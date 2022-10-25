ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-alpine AS linter-base
RUN apk add --no-cache shadow
# UID of current user who runs the build
ARG user_id
# GID of current user who runs the build
ARG group_id
# GID of current docker group of the host
ARG docker_group_id
# HOME of current user who runs the build
ARG home
# change GID for dialout group which collides with MacOS staff GID (20) and
# create group and user to match permmisions of current who runs the build
ARG workdir
WORKDIR ${workdir}
RUN groupmod -g 64 dialout \
    && addgroup -S -g "${group_id}" union \
    && groupmod -g 2999 ping \
    && addgroup -S -g "${docker_group_id}" docker \
    && mkdir -p "${home}" \
    && adduser -S -u "${user_id}" -h "${home}" -s "/bin/bash" -G union builder \
    && gpasswd --add builder docker \
    && chown -R builder:union "${workdir}"


FROM linter-base AS pipenv
RUN apk add --no-cache \
    bash \
    curl \
    docker \
    gcc \
    git \
    libc-dev \
    make \
    && pip install pipenv
USER builder
# Install Python dependencies so they are cached
ARG workdir
WORKDIR ${workdir}
COPY --chown=builder:union Pipfile Pipfile.lock ./
RUN pipenv install --ignore-pipfile --dev
ENTRYPOINT [ "/usr/local/bin/pipenv" ]

FROM mvdan/shfmt AS shfmt
ENTRYPOINT [ "/bin/shfmt" ]
