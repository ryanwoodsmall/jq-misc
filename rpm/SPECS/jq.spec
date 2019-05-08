%define debug_package     %{nil}
%define oniguruma_version 6.9.2
%define oniguruma_dir     onig-%{oniguruma_version}

Name:           jq
Version:        1.6
Release:        14%{?dist}
Summary:        Command-line JSON processor

License:        MIT and ASL 2.0 and CC-BY and GPLv3
URL:            http://stedolan.github.io/jq/
Source0:        https://github.com/stedolan/jq/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/kkos/oniguruma/releases/download/v%{oniguruma_version}/onig-%{oniguruma_version}.tar.gz

BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  glibc-static
BuildRequires:  musl-static >= 1.1.22
BuildRequires:  ruby >= 1.8

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
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}


%prep
%setup -qn %{name}-%{version}

%build
cd modules
rm -rf oniguruma
tar -zxf %{SOURCE1}
mv %{oniguruma_dir} oniguruma
cd ..
%configure \
  --enable-static \
  --enable-static=yes \
  --disable-shared \
  --enable-shared=no \
  --disable-maintainer-mode \
  --enable-all-static \
  --disable-silent-rules \
  --disable-valgrind \
  --with-oniguruma=builtin \
    CC="musl-gcc" CFLAGS="-fPIC"
find modules/oniguruma -name Makefile \
| xargs sed -i.ORIG '/AM_CPPFLAGS/s/\$(includedir)/./g'
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
rm -f %{buildroot}%{_includedir}/onig*.h
rm -f %{buildroot}%{_bindir}/onig*
rm -f %{buildroot}%{_libdir}/libonig.*
rm -f %{buildroot}%{_libdir}/pkgconfig/onig*

%check
# Valgrind used, so restrict architectures for check
%ifarch %{ix86} x86_64
make check V=1
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/%{name}
%{_datadir}/man/man1/jq.1.gz
%{_datadir}/doc/jq/AUTHORS
%{_datadir}/doc/jq/COPYING
%{_datadir}/doc/jq/README
%{_datadir}/doc/jq/README.md

%files devel
%{_includedir}/jq.h
%{_includedir}/jv.h
%{_libdir}/libjq.a

%changelog
* Tue May  7 2019 ryan woodsmall <rwoodsmall@gmail.com> - 1.6-14
- release bump for oniguruma 6.9.2

* Thu Apr 11 2019 ryan woodsmall <rwoodsmall@gmail.com> - 1.6-13
- release bump for musl 1.1.22

* Tue Jan 22 2019 ryan woodsmall <rwoodsmall@gmail.com> - 1.6-12
- release no. bump for musl 1.1.21

* Sun Dec 23 2018 ryan woodsmall <rwoodsmall@gmail.com> - 1.6-11
- update oniguruma to 6.9.1

* Wed Nov  7 2018 ryan woodsmall <rwoodsmall@gmail.com> - 1.6-10
- use builtin onigurma support
- unholy

* Wed Nov  7 2018 ryan woodsmall <rwoodsmall@gmail.com> - 1.6-9
- update to jq 1.6

* Tue Sep 11 2018 ryan woodsmall <rwoodsmall@gmail.com> - 1.5-9
- release no. bump for oniguruma 6.9.0

* Tue Sep 11 2018 ryan woodsmall <rwoodsmall@gmail.com> - 1.5-8
- release no. bump for musl 1.1.20

* Fri Apr 20 2018 ryan woodsmall <rwoodsmall@gmail.com> - 1.5-7
- oniguruma 6.8.2

* Sun Apr  1 2018 ryan woodsmall <rwoodsmall@gmail.com> - 1.5-6
- oniguruma 6.8.1

* Thu Feb 22 2018 ryan woodsmall <rwoodsmall@gmail.com> - 1.5-5
- musl-libc 1.1.19
- oniguruma 6.7.1

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
