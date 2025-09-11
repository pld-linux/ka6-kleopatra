#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.1
%define		kframever	6.13.0
%define		qtver		6.8
%define		kaname		kleopatra
Summary:	GUI for GnuPG
Name:		ka6-%{kaname}
Version:	25.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	796d6e044d71a6f4e2f324aeb228e0aa
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Network-devel >= 5.11.1
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	gpgmepp-devel >= 1.23.2
BuildRequires:	ka6-kmime-devel >= %{kdeappsver}
BuildRequires:	ka6-libkleo-devel >= %{kdeappsver}
BuildRequires:	ka6-mimetreeparser-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcolorscheme-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kitemmodels-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	libassuan-devel >= 2.4.2
BuildRequires:	libgpg-error-devel >= 1.36
BuildRequires:	ninja
BuildRequires:	qgpgme-qt6-devel >= 1.23.2
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kleopatra is a GUI for GnuPG.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.packagers
/etc/xdg/kleopatradebugcommandsrc
%attr(755,root,root) %{_bindir}/kleopatra
%attr(755,root,root) %{_bindir}/kwatchgnupg
%{_desktopdir}/kleopatra_import.desktop
%{_desktopdir}/org.kde.kleopatra.desktop
%{_desktopdir}/org.kde.kwatchgnupg.desktop
%{_iconsdir}/hicolor/*x*/apps/*.png
%{_iconsdir}/hicolor/scalable/apps/kleopatra.svg
%{_iconsdir}/hicolor/scalable/apps/org.kde.kwatchgnupg.svg
%{_datadir}/kio/servicemenus/kleopatra_decryptverifyfiles.desktop
%{_datadir}/kio/servicemenus/kleopatra_signencryptfiles.desktop
%{_datadir}/kio/servicemenus/kleopatra_signencryptfolders.desktop
%{_datadir}/metainfo/org.kde.kleopatra.appdata.xml
%{_datadir}/mime/packages/application-vnd-kde-kleopatra.xml
%{_datadir}/mime/packages/kleopatra-mime.xml
%{_datadir}/qlogging-categories6/kleopatra.categories
%{_datadir}/qlogging-categories6/kleopatra.renamecategories
