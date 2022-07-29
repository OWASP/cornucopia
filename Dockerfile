ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim AS pipenv
ARG workdir
WORKDIR ${workdir}
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
COPY Pipfile Pipfile.lock ./
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pip install types-PyYAML && pipenv install --dev --system --deploy
ENTRYPOINT [ "/usr/local/bin/pipenv" ]

FROM mvdan/shfmt AS shfmt
ENTRYPOINT [ "/bin/shfmt" ]

FROM koalaman/shellcheck AS shellcheck
ENTRYPOINT [ "/bin/shellcheck" ]
