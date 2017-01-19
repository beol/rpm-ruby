FROM centos:centos6
MAINTAINER Leo Laksmana <beol@laksmana.com>

RUN yum -y install \
           automake \
           autoconf \
           bison \
           bzip2 \
           expect \
           gcc-c++ \
           glibc-devel \
           libffi-devel \
           libtool \
           libyaml \
           libyaml-devel \
           m4 \
           make \
           openssl \
           openssl-devel \
           patch \
           perl \
           readline \
           readline-devel \
           rpm-build \
           rpmdevtools \
           sqlite-devel \
           vim-enhanced \
           zlib \
           zlib-devel


WORKDIR /etc/pki/rpm-gpg
COPY RPM-GPG-KEY-laksmana .
RUN rpm --import RPM-GPG-KEY-laksmana

WORKDIR /
RUN useradd -m -d /source -u 1000 rpmbuild

WORKDIR /source
USER rpmbuild
