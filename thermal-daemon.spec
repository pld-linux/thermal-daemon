Summary:	The "Linux Thermal Daemon" program from 01.org
Name:		thermal-daemon
Version:	1.3
Release:	1
License:	GPL v2+
Group:		Base
# TODO: use "%{name}-%{version}.tar.gz" as filename when updating version
Source0:	https://github.com/01org/thermal_daemon/archive/v%{version}/v%{version}.tar.gz
# Source0-md5:	d80f6dd4e8c080cdeaa943afbfa87523
URL:		https://github.com/01org/thermal_daemon
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	glib2-devel
BuildRequires:	libxml2-devel
BuildRequires:	rpmbuild(macros) >= 1.671
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Thermal Daemon monitors and controls platform temperature.

%prep
%setup -q -n thermal_daemon-%{version}

%build
install -d build-aux
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post thermald.service

%preun
%systemd_preun thermald.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README.txt
%dir %{_sysconfdir}/thermald
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/thermald/thermal-conf.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/thermald/thermal-cpu-cdev-order.xml
%config(noreplace) /etc/dbus-1/system.d/org.freedesktop.thermald.conf
%attr(755,root,root) %{_sbindir}/thermald
%{_datadir}/dbus-1/system-services/org.freedesktop.thermald.service
%{_mandir}/man5/thermal-conf.xml.5*
%{_mandir}/man8/thermald.8*
%{systemdunitdir}/thermald.service
