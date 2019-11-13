%define major 1
%define girapi %{major}.0
%define libname %mklibname modulemd %{major}
%define girname %mklibname modulemd-gir %{girapi}
%define devname %mklibname modulemd%{major} -d

%bcond_without gir
%bcond_with gtk-doc

Summary:	Library for manipulating module v1 metadata files
Name:		modulemd%{major}
Version:	%{major}.8.16
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/fedora-modularity/%{name}
Source0:	https://github.com/fedora-modularity/libmodulemd/archive/modulemd-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	python3egg(autopep8)
BuildRequires:	python3dist(pygobject)
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	magic-devel
BuildRequires:	/bin/sh
BuildRequires:	sed
BuildRequires:	coreutils
%if %{with gtk-doc}
BuildRequires:	gtk-doc
%endif
#BuildRequires:	valgrind
%rename libmodulemd%{major}

%description
Library for manipulating module v1 metadata files

%package -n %{libname}
Summary:	Library for manipulating module v1 metadata files
Group:		System/Libraries

%description -n %{libname}
Library for manipulating module v1 metadata files

%package -n %{girname}
Summary:	GObject Introspection interface description for libmodulemd%{major}
Group:		System/Libraries
Requires:	%{libname}%{?_isa} = %{EVRD}

%description -n %{girname}
GObject Introspection interface description for libmodulemd%{major}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	lib%{name}-devel%{?_isa} = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Requires:	%{girname}%{?_isa} = %{EVRD}
Requires:	%{libname}%{?_isa} = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%prep
%autosetup -p1 -n modulemd-%{version}

%build
%meson \
%if !%{with gir}
	-Dskip_introspection=true \
%endif
%if %{without gtk-doc}
	-Dwith_docs=false \
%endif
	-Ddeveloper_build=false

%ninja_build -C build

%install
%ninja_install -C build

%files
%{_bindir}/modulemd-validator-v1

%files -n %{libname}
%{_libdir}/libmodulemd.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Modulemd-%{girapi}.typelib

%files -n %{devname}
%license COPYING
%{_libdir}/libmodulemd.so
%{_datadir}/gir-1.0/Modulemd-%{girapi}.gir
%{_includedir}/modulemd
%{_libdir}/pkgconfig/modulemd.pc
%if %{with gtk-doc}
%doc %{_datadir}/gtk-doc/html/modulemd-%{girapi}
%endif
