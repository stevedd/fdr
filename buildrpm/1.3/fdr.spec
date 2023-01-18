Summary:	A daemon which enables ftrace probes and harvests the data
Name:		fdr
URL:		https://github.com/oracle/fdr.git
Version:	1.3
Release:	3%{?dist}
License:	UPL

Source0:	http://people.redhat.com/steved/fdr/%{name}-%{version}.tar.xz

BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	sed
BuildRequires:	systemd-rpm-macros
Requires:	systemd logrotate

%description
The flight data recorder, a daemon which enables ftrace probes
and harvests the data

%prep
%autosetup

%build
sed -i -e "s:^CFLAGS.*:CFLAGS = %{optflags}:" Makefile
%make_build


%install
mkdir -p %{buildroot}/%{_sbindir}
install -m 755 fdrd %{buildroot}/%{_sbindir}

mkdir -p %{buildroot}%{_datadir}/fdr/samples
install -m 644 samples/nfs %{buildroot}/%{_datadir}/fdr/samples
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 samples/nfs.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/nfs

mkdir -p %{buildroot}/%{_unitdir}
install -m 644 %{name}d.service %{buildroot}/%{_unitdir}/%{name}d.service

mkdir -p %{buildroot}%{_sysconfdir}/%{name}.d
install -m 644 configs/nfsall.conf %{buildroot}%{_sysconfdir}/%{name}.d/

mkdir -p %{buildroot}/%{_mandir}/man8
install -m 644 fdrd.man %{buildroot}/%{_mandir}/man8/fdrd.8

%post
%systemd_post %{name}d.service

%preun
%systemd_preun %{name}d.service

%postun
%systemd_postun_with_restart %{name}d.service

%files
%{_sbindir}/fdrd
%{_unitdir}/fdrd.service
%{_datadir}/fdr/samples/nfs
%{_sysconfdir}/logrotate.d/nfs
%{_sysconfdir}/%{name}.d
%{_sysconfdir}/%{name}.d/nfsall.conf
%{_mandir}/man8/*
%doc README.md
%license LICENSE

%changelog
* Fri Jun 25 2021 Bill Baker <webbaker@gmail.com>  1.3-2
- Initial commit
