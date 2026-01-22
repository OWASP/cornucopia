FROM python:3.12.12-alpine3.22@sha256:d82291d418d5c47f267708393e40599ae836f2260b0519dd38670e9d281657f5 AS pipenv
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
RUN pip install pipenv
USER builder
# Install Python dependencies so they are cached
ARG workdir
WORKDIR ${workdir}
COPY --chown=builder:union Pipfile Pipfile.lock ./
RUN pipenv --python "$(which python)" install --ignore-pipfile --dev
ENTRYPOINT ["/usr/local/bin/pipenv"]

FROM mvdan/shfmt@sha256:9e915e1d22ad71a19a869cfe922127944783dd54406d9ebfb1c3115a26122279 AS shfmt
ENTRYPOINT ["/bin/shfmt"]