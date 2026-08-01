DOCKER = docker run \
	--interactive \
	--rm \
	--env "HOST_IP=$(HOST_IP)" \
	--env "MYPYPATH=${PWD}/typings" \
	--env "RETRY_DELAY=${RETRY_DELAY}" \
	--env "UPDATE_GOLDEN_FILES=$(UPDATE_GOLDEN_FILES)" \
	--volume "$(PWD):${PWD}" \
	--volume "/var/run/docker.sock:/var/run/docker.sock" \
	--workdir "${PWD}"

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -O globstar -c

HOST_IP ?= $(shell ip addr show dev docker0 | grep -oP "(?<=inet )[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
RETRY_DELAY = 0.01

PYTHON_TEST_PATTERN ?= "*_?test.py" # Default to all types of tests
PYTHON_COVERAGE_MIN = 85 # %

.PHONY: shfmt shellcheck pipenv
shfmt shellcheck pipenv:
	@docker build \
		--tag $@ \
		--build-arg "user_id=$(shell id -u)" \
		--build-arg "group_id=$(shell id -g)" \
		--build-arg "home=${HOME}" \
		--build-arg "workdir=${PWD}" \
		--target $@ . \
		>/dev/null

.PHONY: fmt
fmt: shfmt pipenv
	@$(DOCKER) shfmt -l -w .
	@$(DOCKER) pipenv run black --line-length=120 .

.PHONY: fmt-check
fmt-check: shfmt pipenv
	@$(DOCKER) shfmt -d .
	@$(DOCKER) pipenv run black --line-length=120 --check .

.PHONY: static-check
static-check: pipenv
	@$(DOCKER) pipenv run flake8 --max-line-length=120 --max-complexity=10 --ignore=E203,W503 --exclude ./.venv/
	@$(DOCKER) pipenv run mypy --namespace-packages --strict ./scripts/

.PHONY: coverage-check
coverage-check: python-coverage-only

.PHONY: test
test: python-unit-test python-integration-test coverage-check
	@$(MAKE) -C docker smoke-test

.PHONY: python-test
python-test: pipenv
	@$(DOCKER) pipenv run coverage run \
		--append \
		--branch \
		--omit "*_?test.py,*/.local/*" \
		--module unittest \
			discover \
			--verbose \
			--start-directory "tests/scripts" \
			--pattern $(PYTHON_TEST_FILE)$(PYTHON_TEST_PATTERN)

.PHONY: python-unit-test
python-unit-test:
	@$(MAKE) python-test PYTHON_TEST_PATTERN="*_utest.py" PYTHON_TEST_FILE=$(PYTHON_TEST_FILE)

.PHONY: python-integration-test
python-integration-test:
	@$(MAKE) python-test PYTHON_TEST_PATTERN="*_itest.py" PYTHON_TEST_FILE=$(PYTHON_TEST_FILE)

.PHONY: python-coverage-only
python-coverage-only:
	@$(DOCKER) pipenv run coverage xml
	@$(DOCKER) pipenv run coverage report --fail-under $(PYTHON_COVERAGE_MIN)

.PHONY: python-coverage
python-coverage:
	-@rm .coverage
	@$(MAKE) python-unit-test
	@$(MAKE) python-integration-test
	@$(MAKE) python-coverage-only

.PHONY: python-test-update-golden-files
python-test-update-golden-files:
	UPDATE_GOLDEN_FILES=true $(MAKE) python-unit-test PYTHON_TEST_FILE=$(PYTHON_TEST_FILE)
	UPDATE_GOLDEN_FILES=true $(MAKE) python-integration-test PYTHON_TEST_FILE=$(PYTHON_TEST_FILE)

.PHONY: google-account
google-account:

.PHONY: release
release:
	@rm -f .version.properties
	git tag -d pre-release 2> /dev/null || echo ok
	git checkout master
	git fetch --all
	git pull origin master
	./version-up.sh --patch -r --prefix v --apply
	@rm -f .version.properties
	# To release a new version:
	# git push origin --tag <name of tag>
.PHONY: release-patch
release-patch:
	@rm -f .version.properties
	git tag -d pre-release 2> /dev/null || echo ok
	git checkout master
	git fetch --all
	git pull origin master
	./version-up.sh --patch -r --prefix v --apply
	@rm -f .version.properties
	#
	# To release a new version:
	# git push origin --tag <name of tag>
.PHONY: release-minor
release-minor:
	@rm -f .version.properties
	git tag -d pre-release 2> /dev/null || echo ok
	git checkout master
	git fetch --all
	git pull origin master
	./version-up.sh --minor -r --prefix v --apply
	@rm -f .version.properties
	#
	# To release a new version:
	# git push origin --tag <name of tag>
.PHONY: release-major
release-major:
	@rm -f .version.properties
	git tag -d pre-release 2> /dev/null || echo ok
	git checkout master
	git fetch --all
	git pull origin master
	./version-up.sh --major -r --prefix v --apply
	@rm -f .version.properties
	# 
	# To release a new version:
	# git push origin --tag <name of tag>
.PHONY: ready
ready: fmt static-check python-coverage
