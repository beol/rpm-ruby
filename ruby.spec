%global _name   ruby
%global rubyver %{?_version}%{!?_version:2.1.10}
%global rubyxver    %(echo %{rubyver} | cut -d. -f1,2)
%global _prefix /opt/%{name}

Name: 		%{_name}%(echo %{rubyxver} | sed 's,\.,,')
Version: 	%{rubyver}
Release: 	%{?_release}%{!?_release:0a}%{?dist}
Summary:  	An interpreter of object-oriented scripting language
License: 	BSDL & GPL -- see COPYING
Group: 		Development/Languages
URL:    	http://ruby-lang.org/
Source: 	https://cache.ruby-lang.org/pub/ruby/%{rubyxver}/%{_name}-%{version}.tar.gz
BuildRequires:	automake autoconf bison gcc-c++ glibc-devel libffi-devel
BuildRequires:	libtool libyaml-devel m4 make openssl-devel patch perl 
BuildRequires:	readline-devel sqlite-devel zlib-devel
BuildRoot:	%{_tmppath}/%{_name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	bzip2 readline openssl zlib
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Provides:   ruby = %{version}-%{release}
Provides:   ruby(abi) = %{rubyxver}
Provides:   libruby = %{version}-%{release}
Provides:   ruby-libs = %{version}-%{release}
Provides:   ruby-devel = %{version}-%{release}
Provides:   irb = %{version}-%{release}
Provides:   rdoc = %{version}-%{release}
Provides:   ri = %{version}-%{release}
Provides:   rubygems

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -q -n %{_name}-%{version}

%build
./configure \
    --prefix=%{_prefix} \
    --enable-shared \
    --disable-rpath \
    --disable-install-doc \
    --with-soname=%{name} \
    --without-tcl \
    --without-X11

make %{_smp_mflags} \
    all

%install
rm -rf $RPM_BUILD_ROOT
make %{_smp_mflags} DESTDIR=$RPM_BUILD_ROOT \
    INSTALLDIRS=vendor install

rm -rf $RPM_BUILD_ROOT%{_datadir}
find $RPM_BUILD_ROOT%{_prefix} -name lib%{name}-static.a -exec rm -f {} \;

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/lib%{name}.conf
%{_prefix}/lib/
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc BSDL README README.ja LEGAL GPL COPYING COPYING.ja
%{_prefix}
%{_sysconfdir}/ld.so.conf.d/lib%{name}.conf

