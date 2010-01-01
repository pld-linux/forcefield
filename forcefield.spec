#
# TODO:
# - real descriptions
# - check BR-s and R-s
#
%define     _snap   20070924
Summary:	A GNOME GUI for TrueCrypt
Summary(pl.UTF-8):	Graficzny interfejs GNOME do TrueCrypta
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
Patch0:		%{name}-install.patch
Patch1:		%{name}-cracklib.patch
URL:		http://www.bockcay.de/forcefield
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	python >= 1:2.5
BuildRequires:	python-gnome-devel
BuildRequires:	python-pygtk-devel >= 2:2.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sed >= 4.0
Requires(post,preun):	GConf2 >= 2.4.0
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
%pyrequires_eq	python
Requires:	cracklib
Requires:	python-cracklib
Requires:	python-gnome
Requires:	python-gnome-extras
Requires:	python-gnome-gconf
Requires:	python-pexpect
Requires:	python-pygtk-glade >= 2:2.0
Requires:	python-pygtk-gtk >= 2:2.0
Requires:	python-pynotify
Requires:	truecrypt
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A GNOME GUI for TrueCrypt.

%description -l pl.UTF-8
Graficzny interfejs GNOME do TrueCrypta.

%prep
%setup -q -n %{name}-%{_snap}
%patch0 -p1
%patch1 -p1

sed -i -e 's|include/python2.4|include/python%{py_ver} $(CFLAGS) -fPIC|g' src/lib/Makefile.am
# kill precompiled x86 module
rm data/misc/crack.so

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%py_postclean
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install %{name}.schemas
%update_icon_cache hicolor
%update_mime_database

%preun
%gconf_schema_uninstall %{name}.schemas

%postun
%update_icon_cache hicolor
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/%{name}
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{name}/zero_out.so
%{_datadir}/%{name}
%{_iconsdir}/hicolor/24x24/apps/%{name}.png
%{_desktopdir}/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
