ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-alpine AS linter-base
RUN apk add --no-cache shadow~=4.8.1
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
    && addgroup -S \
    -g "${group_id}" \
    union \
    && groupmod -g 2999 ping \
    && addgroup -S \
    -g "${docker_group_id}" \
    docker \
    && mkdir -p "${home}" \
    && adduser -S \
    -u "${user_id}" \
    -h "${home}" \
    -s "/bin/bash" \
    -G union \
    builder \
    && gpasswd --add builder docker \
    && chown -R builder:union "${workdir}"

FROM linter-base AS shfmt
ARG SHFMT_VERSION=3.1.2
RUN wget -qO /bin/shfmt \
    "https://github.com/mvdan/sh/releases/download/v${SHFMT_VERSION}/shfmt_v${SHFMT_VERSION}_linux_amd64" \
    && chmod a+x /bin/shfmt
USER builder
ENTRYPOINT [ "/bin/shfmt" ]

FROM linter-base AS shellcheck
SHELL ["/bin/ash", "-o", "pipefail", "-c"]
ARG SHELLCHECK_VERSION=0.7.1
RUN apk add --no-cache xz~=5.2 && \
    wget -qO- \
        "https://github.com/koalaman/shellcheck/releases/download/v${SHELLCHECK_VERSION}/shellcheck-v${SHELLCHECK_VERSION}.linux.x86_64.tar.xz" \
    | tar -C /bin --strip-components 1 -xJv "shellcheck-v${SHELLCHECK_VERSION}/shellcheck"
USER builder
ENTRYPOINT [ "/bin/shellcheck" ]

FROM linter-base AS pipenv
RUN apk add --no-cache \
    bash=~5.0 \
    curl=~7.77 \
    docker~=20.10 \
    gcc~=9.3 \
    git~=2.26 \
    libc-dev~=0.7 \
    libxml2-dev=~2.9 \
    python3-dev=~3.8 \
    libxslt-dev \
    libffi-dev \
    make=~4.3 \
    && pip install pipenv==2021.5.29
USER builder
# Install Python dependencies so they are cached
ARG workdir
WORKDIR ${workdir}
COPY --chown=builder:union Pipfile Pipfile.lock ./
RUN pipenv install --ignore-pipfile --dev
ENTRYPOINT [ "/usr/local/bin/pipenv" ]
