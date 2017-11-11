%define		debug_package		%{nil}
%define		oniguruma_version	6.6.1
%define		oniguruma_dir		onig-%{oniguruma_version}

Name:           jq
Version:        1.5
Release:        4%{?dist}
Summary:        Command-line JSON processor

License:        MIT and ASL 2.0 and CC-BY and GPLv3
URL:            http://stedolan.github.io/jq/
Source0:        https://github.com/stedolan/jq/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/kkos/oniguruma/releases/download/v%{oniguruma_version}/onig-%{oniguruma_version}.tar.gz

BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  oniguruma-devel
BuildRequires:  glibc-static
BuildRequires:  musl-static
BuildRequires:	ruby >= 1.8

%ifarch %{ix86} x86_64
BuildRequires:  valgrind
%endif


%description
lightweight and flexible command-line JSON processor

 jq is like sed for JSON data – you can use it to slice
 and filter and map and transform structured data with
 the same ease that sed, awk, grep and friends let you
 play with text.

 It is written in portable C, and it has zero runtime
 dependencies.

 jq can mangle the data format that you have into the
 one that you want with very little effort, and the
 program to do so is often shorter and simpler than
 you'd expect.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}


%prep
%setup -qn %{name}-%{version}

%build
# build a static oniguruma
tar -zxf %{SOURCE1}
cd %{oniguruma_dir}
./configure \
  --prefix=${PWD}-built \
  --enable-shared=no \
  --disable-shared \
  --enable-static \
  --enable-static=yes \
    CC="musl-gcc"
make %{?_smp_mflags}
make install-strip
cd ..
# % configure --disable-static --disable-maintainer-mode
%configure \
  --enable-static \
  --enable-static=yes \
  --disable-shared \
  --enable-shared=no \
  --disable-maintainer-mode \
  --enable-all-static \
  --disable-silent-rules \
  --disable-valgrind \
  --with-oniguruma="${PWD}/%{oniguruma_dir}-built" \
    CC="musl-gcc" CFLAGS="-fPIC"
make %{?_smp_mflags}
# Docs already shipped in jq's tarball.
# In order to build the manual page, it
# is necessary to install rake, rubygem-ronn
# and do the following steps:
#
# # yum install rake rubygem-ronn
# $ cd docs/
# $ curl -L https://get.rvm.io | bash -s stable --ruby=1.9.3
# $ source $HOME/.rvm/scripts/rvm
# $ bundle install
# $ cd ..
# $ ./configure
# $ make real_docs

%install
make DESTDIR=%{buildroot} install-strip
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%check
# Valgrind used, so restrict architectures for check
%ifarch %{ix86} x86_64
make check V=1
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/%{name}
# % {_libdir}/libjq.so.*
%{_datadir}/man/man1/jq.1.gz
%{_datadir}/doc/jq/AUTHORS
%{_datadir}/doc/jq/COPYING
%{_datadir}/doc/jq/README
%{_datadir}/doc/jq/README.md

%files devel
%{_includedir}/jq.h
%{_includedir}/jv.h
# % {_libdir}/libjq.so
%{_libdir}/libjq.a

%changelog
* Fri Nov 10 2017 ryan woodsmall <rwoodsmall@gmail.com> - 1.5-4
- update oniguruma to 6.6.1

* Tue Jan 31 2017 ryan woodsmall <rwoodsmall@gmail.com> - 1.5-3
- do "make install-strip" so we don't get unstripped binaries

* Tue Jan 31 2017 ryan woodsmall <rwoodsmall@gmail.com> - 1.5-2
- static build using musl and local oniguruma

* Tue Aug 25 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1.5-1
- Upstream 1.5.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 24 2013 Flavio Percoco <flavio@redhat.com> - 1.3-2
- Added check, manpage

* Fri Oct 18 2013 Flavio Percoco <flavio@redhat.com> - 1.3-1
- Initial package release.
