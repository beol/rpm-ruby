#!/bin/env bash

set -ev

BASE_DIR=$(dirname $0)

rpmbuild -bb ${BASE_DIR}/ruby.spec
