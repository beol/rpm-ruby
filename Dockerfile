FROM centos:centos6

RUN yum -y install \
           automake \
           bison \
           bzip2 \
           expect \
           gcc-c++ \
           glibc-devel \
           libffi-devel \
           libtool \
           libyaml-devel \
           m4 \
           make \
           openssl-devel \
           patch \
           perl \
           readline \
           readline-devel \
           rpm-build \
           sqlite-devel \
           zlib \
           zlib-devel


WORKDIR /etc/pki/rpm-gpg
COPY RPM-GPG-KEY-laksmana .
RUN rpm --import RPM-GPG-KEY-laksmana

WORKDIR /tmp
ADD http://ftp.gnu.org/gnu/autoconf/autoconf-2.67.tar.gz .
RUN tar xvzf autoconf-2.67.tar.gz
RUN rm -f autoconf-2.67.tar.gz
RUN cd autoconf-2.67; ./configure && make && make install

WORKDIR /
RUN useradd -m -d /source -u 1000 rpmbuild

WORKDIR /source
USER rpmbuild
