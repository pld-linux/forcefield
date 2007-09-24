#
# TODO:
# - more meaningful translation
# - check BR-s and R-s
# - investigate if the cracklib patch realy make forcefield *not*
#   require python-crypt
# - correct update_icons
#
%define     _snap   20070924
Summary:	A GNOME GUI for TrueCrypt
Summary(pl.UTF-8):GNOME-owe GUI dla TrueCrypta
Name:		forcefield
Version:	0.92
Release:	0.%{_snap}
License:	GPL
Group:		Applications/System
# Download current version with: svn checkout
# http://bockcay.de/svn/forcefield/trunk
Source0:	%{name}-%{_snap}.tar.bz2
# Source0-md5:	6e403a32487c24eeb0fea2ec30500276
Source1:	%{name}.desktop
URL:		http://www.bockcay.de/forcefield
Patch0:		%{name}-install.patch
Patch1:		%{name}-cracklib.patch
BuildRequires:	automake >= 1.9
BuildRequires:	python >= 2.5
BuildRequires:	python-gnome-devel
BuildRequires:	python-pygtk-devel
Requires:	GConf2 >= 2.4.0
Requires:	cracklib
Requires:	python >= 2.5
Requires:	python-cracklib
Requires:	python-gnome
Requires:	python-gnome-extras
Requires:	python-gnome-gconf
Requires:	python-pexpect
Requires:	python-pygtk-glade
Requires:	python-pygtk-gtk
Requires:	python-pynotify
Requires:	truecrypt
BuildArch:	noarch
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A GNOME GUI for TrueCrypt.

%description -l pl.UTF-8
GNOME-owe GUI dla TrueCrypta.

%prep
%setup -q -n %{name}-%{_snap}
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__perl} -pi -e 's|python2.4|python2.5|g' src/lib/Makefile.in
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install %{name}.schemas
%update_icon_cache
%update_mime_database hicolor

%postun
%gconf_schema_uninstall
%update_mime_database hicolor


%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/%{name}
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*.py[co]
%{py_sitedir}/%{name}/*.so
%{_datadir}/%{name}
%{_iconsdir}/hicolor/24x24/apps/%{name}.png
%{_desktopdir}/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
