# Pass --without docs to rpmbuild if you don't want the documentation
%global _name   ruby
%global majorver 2
%global minorver 3
%global patchver 1
%global packagename %{_name}%{majorver}%{minorver}
%global _prefix /opt/%{name}

Name: 		%{packagename}
Version: 	%{majorver}.%{minorver}.%{patchver}
Release: 	%(echo ${RELEASE_VERSION:-0a})%{?dist}
Summary:  	Core git tools
License: 	GPL
Group: 		Development/Tools
URL:    	https://cache.ruby-lang.org/pub/ruby/
Source: 	https://cache.ruby-lang.org/pub/ruby/%{majorver}.%{minorver}/%{_name}-%{version}.tar.gz
BuildRequires:	automake autoconf bison gcc-c++ glibc-devel libffi-devel
BuildRequires:	libtool m4 make openssl-devel patch perl readline-devel
BuildRequires:	sqlite-devel zlib-devel
BuildRoot:	%{_tmppath}/%{_name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	bzip2, readline, openssl, zlib 
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -q -n %{_name}-%{version}

%build
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     configure
./configure --prefix=%{_prefix} \
            --enable-shared \
            --disable-rpath \
            --disable-install-doc \
            --with-soname=ruby23 \
            --without-gdbm \
            --with-out-ext=tcl \
            --with-out-ext=tk \
            --without-x11

make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fPIC" \
     all

%install
rm -rf $RPM_BUILD_ROOT
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=$RPM_BUILD_ROOT \
     INSTALLDIRS=vendor install \
     NO_GETTEXT=YesPlease

rm -rf $RPM_BUILD_ROOT%{_datadir}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/libruby23.conf
/opt/ruby23/lib/
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig -v

%postun
/sbin/ldconfig -v

%files
%defattr(-,root,root)
%doc BSDL README.md README.ja.md LEGAL GPL COPYING COPYING.ja
%{_prefix}
%{_sysconfdir}/ld.so.conf.d/libruby23.conf

