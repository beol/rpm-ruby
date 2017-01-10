#!/bin/env bash

set -ev

BASE_DIR=$(dirname $0)

rpmbuild -bb ${BASE_DIR}/ruby.spec

find ${BASE_DIR}/rpmbuild/RPMS -type f -name "*.rpm" | \
    xargs -I{} sh -c "${BASE_DIR}/rpm-sign.exp {} && rpm --checksig {}"
