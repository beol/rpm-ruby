#!/bin/env bash

set -ev

BASE_DIR="$(dirname $0)"
VERSION="${1:-2.3.1}"
RELEASE="${2:-0a}"

mkdir -p "${BASE_DIR}/rpmbuild/SOURCES"
[[ -f "${BASE_DIR}/rpmbuild/SOURCES/ruby-${VERSION}.tar.gz" ]] || \
    curl -# -L -o "${BASE_DIR}/rpmbuild/SOURCES/ruby-${VERSION}.tar.gz" "https://cache.ruby-lang.org/pub/ruby/$(echo ${VERSION} | cut -d. -f1,2)/ruby-${VERSION}.tar.gz"

rpmbuild -bb --define "_version ${VERSION}" --define "_release ${RELEASE}" ${BASE_DIR}/ruby.spec

[[ -n "${GPG_PASSPHRASE}" ]] && find ${BASE_DIR}/rpmbuild/RPMS -type f -name "*.rpm" | xargs -I{} sh -c "${BASE_DIR}/rpm-sign.exp {} && rpm --checksig {}"
