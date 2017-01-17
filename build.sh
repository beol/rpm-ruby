#!/bin/env bash

set -ev

BASE_DIR="$(dirname $0)"
VERSION="${1:-2.1.10}"
RELEASE="${2:-0a}"

cd $BASE_DIR

spectool -g -R --define "_version ${VERSION}" --define "_release ${RELEASE}" ruby.spec
rpmbuild -bb --define "_version ${VERSION}" --define "_release ${RELEASE}" ruby.spec

[[ -n "${GPG_PASSPHRASE}" ]] && find ./rpmbuild/RPMS -type f -name "*.rpm" | xargs -I{} sh -c "./rpm-sign.exp {} && rpm --checksig {}"
