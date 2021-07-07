#!/usr/bin/env bash

#
# Interactively decide what version number to use for a release and create and
# push that tag in git
#

set -o errexit  # Exit immediately if any command or pipeline of commands fails
set -o nounset  # Treat unset variables and parameters as an error
set -o pipefail # Exit when command before pipe fails
# set -o xtrace   # Debug mode expand everything and print it before execution

cd "$(dirname "${0}")" # Always run from script location

# Print message to STDERR and exit with non-zero code
error() {
    set -o errexit
    echo "ERROR: ${1}" >&2
    exit 1
}

# Set global variable PROPOSED_VERSION based on given latest_version and
# answers from a user
set_proposed_version() {
    set -o errexit
    local latest_version="${1}"

    # Split version by
    local latest_major
    latest_major=$(cut --delim "." --fields 1 <<< "${latest_version}")
    local latest_minor
    latest_minor=$(cut --delim "." --fields 2 <<< "${latest_version}")
    local latest_patch
    latest_patch=$(cut --delim "." --fields 3 <<< "${latest_version}")

    # Ask questions to determine new value of PROPOSED_VERSION
    local major_increase
    while ! [[ "${major_increase:-}" =~ (yes|no) ]]; do
        read \
            -p $'Does this release contains breaking changes from user point of view? [yes|no]: ' \
            -r \
            major_increase
    done
    if [[ "${major_increase}" == "yes" ]]; then
        PROPOSED_VERSION="$(("${latest_major}" + 1)).0.0"
        return
    fi

    local minor_increase
    while ! [[ "${minor_increase:-}" =~ (yes|no) ]]; do
        read \
            -p $'Is this release adding new functionality? [yes|no]: ' \
            -r \
            minor_increase
    done
    if [[ "${minor_increase}" == "yes" ]]; then
        PROPOSED_VERSION="${latest_major}.$(("${latest_minor}" + 1)).0"
        return
    fi

    local patch_increase
    while ! [[ "${patch_increase:-}" =~ (yes|no) ]]; do
        read \
            -p $'Is this release only fixing bugs? [yes|no]: ' \
            -r \
            patch_increase
    done
    if [[ "${patch_increase}" == "yes" ]]; then
        PROPOSED_VERSION="${latest_major}.${latest_minor}.$(("${latest_patch}" + 1))"
        return
    fi

    error "no changes, no release"
}

# Verify given proposed version with a user with option to enforce user's own
# version
verify_version_with_user() {
    set -o errexit
    local proposed_version="${1}"

    local version_approval
    while ! [[ "${version_approval:-}" =~ (yes|no) ]]; do
        read \
            -p $'Are you happy with new version '"${proposed_version}"'? [yes|no]: ' \
            -r \
            version_approval
    done
    if [[ "${version_approval}" == "yes" ]]; then
        return
    fi

    local different_version
    while ! [[ "${different_version:-}" =~ (yes|no) ]]; do
        read \
            -p $'Do you want to enforce a different version? [yes|no]: ' \
            -r \
            different_version
    done
    if [[ "${different_version}" == "no" ]]; then
        error "version ${proposed_version} denied by user with no alternative"
    fi

    local new_version
    while ! [[ "${new_version:-}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; do
        read \
            -p $'New version in semver format: ' \
            -r \
            new_version
    done

    PROPOSED_VERSION="${new_version}"
}

# Check if given tag exists in this git repo
tag_exists() {
    set -o errexit
    local tag="${1}"

    # Get all tags from the origin
    git pull --tags > /dev/null

    # If tag exists return 0 AKA success
    if git tag --list | grep "${tag}"; then
        return 0
    fi

    return 1
}

# Create local annotated git tag from given tag
create_tag() {
    set -o errexit
    local tag="${1}"

    git tag \
        --annotate "${tag}" \
        --message "${tag}"
}

# Push given git tag to remote origin
push_tag() {
    set -o errexit
    local tag="${1}"

    git push origin "${tag}"
}

main() {
    set -o errexit

    # Fail if current branch is not master
    if [[ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]]; then
        error "current branch is not master"
    fi

    # Get latest semver version number, eg 1.23.456
    local latest_version
    latest_version="$(git describe \
        --tags \
        --dirty \
        --always \
        2> /dev/null \
        | grep -oE "^[0-9]+\.[0-9]+\.[0-9]+")"
    if [[ -z "${latest_version}" ]]; then
        error "cannot get latest version from the last git tag"
    fi

    echo "The latest version: ${latest_version}"

    set_proposed_version "${latest_version}"

    verify_version_with_user "${PROPOSED_VERSION}"

    if tag_exists "${PROPOSED_VERSION}"; then
        echo "Tag ${PROPOSED_VERSION} already exists. No action needed."
        return
    fi

    create_tag "${PROPOSED_VERSION}"
    push_tag "${PROPOSED_VERSION}"
}

main
