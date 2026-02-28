FROM python:3.14.3-alpine3.22@sha256:b0d9cd5ed77285b2563c86ca10b53578249ca1a08d14e5b69b7970884a9fb539 AS pipenv
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

FROM mvdan/shfmt@sha256:a27f723838dc23a5f818cc6282304e8e7ef2abe2f54f09814a062379e5a2866e AS shfmt
ENTRYPOINT ["/bin/shfmt"]
