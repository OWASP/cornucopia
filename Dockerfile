FROM python:3.14.5-alpine3.22@sha256:6b91e66ab2a880ce9ca5a1b91c70f45963ff71ff68268df056336e1a657d5efd AS pipenv
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
RUN groupmod -g 64 dialout && \
	addgroup -S -g "${group_id}" union && \
	groupmod -g 2999 ping && \
	mkdir -p "${home}" && \
	adduser -S -u "${user_id}" -h "${home}" -s "/bin/bash" -G union builder
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
RUN pip install --no-cache-dir -r requirements.txt --require-hashes
USER builder
# Install Python dependencies so they are cached
ARG workdir
WORKDIR ${workdir}
COPY --chown=builder:union Pipfile Pipfile.lock ./
RUN pipenv --python "$(which python)" install --ignore-pipfile --dev
ENTRYPOINT ["/usr/local/bin/pipenv"]

FROM mvdan/shfmt@sha256:ae73b6336def6bf11d489580555c47f61a773cf55a9a59f6992e2d8f7780f29b AS shfmt
ENTRYPOINT ["/bin/shfmt"]
