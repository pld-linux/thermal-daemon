Summary:	The "Linux Thermal Daemon" program from 01.org
Summary(pl.UTF-8):	Linux Thermal Daemon z 01.org
Name:		thermal-daemon
Version:	2.2
Release:	2
License:	GPL v2+
Group:		Base
Source0:	https://github.com/01org/thermal_daemon/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4e86f9c2fedcdfc10bb2654edcc96414
Patch0:		print-time_t.patch
URL:		https://github.com/01org/thermal_daemon
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-devel >= 1.1
BuildRequires:	dbus-glib-devel >= 0.94
BuildRequires:	glib2-devel >= 1:2.22
BuildRequires:	libxml2-devel >= 2.4
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.671
Requires(post,preun,postun):	systemd-units >= 38
Requires:	dbus >= 1.1
Requires:	dbus-glib >= 0.94
Requires:	glib2 >= 1:2.22
Requires:	libxml2 >= 2.4
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Thermal Daemon monitors and controls platform temperature.

%description -l pl.UTF-8
Thermal Daemon monitoruje i kontroluje temperaturę komputera.

%prep
%setup -q -n thermal_daemon-%{version}
%patch0 -p1

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

cp -p data/thermal-conf.xml $RPM_BUILD_ROOT/%{_sysconfdir}/thermald

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
