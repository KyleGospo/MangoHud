%global appname MangoHud

%global imgui_ver       1.81
%global imgui_wrap_ver  1

# Tests requires bundled stuff. Disable for now.
%bcond_with tests

# Disable unpackaged files check for 32-bit builds shipping with conflicting files
%define _unpackaged_files_terminate_build 0

Name:           mangohud
Version:        100.bazzite.{{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            https://github.com/KyleGospo/MangoHud
Source0:        %{url}/archive/refs/heads/master.zip
Source1:        https://github.com/ocornut/imgui/archive/v%{imgui_ver}/imgui-%{imgui_ver}.tar.gz
Source2:        https://wrapdb.mesonbuild.com/v1/projects/imgui/%{imgui_ver}/%{imgui_wrap_ver}/get_zip#/imgui-%{imgui_ver}-%{imgui_wrap_ver}-wrap.zip

BuildRequires:  appstream
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  SDL2-devel
BuildRequires:  libstdc++-static
BuildRequires:  git-core
BuildRequires:  glslang-devel
BuildRequires:  libappstream-glib
BuildRequires:  mesa-libGL-devel
BuildRequires:  meson >= 0.60
BuildRequires:  python3-mako
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(libdrm)

BuildRequires:  pkgconfig(spdlog)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
BuildRequires:  cmake(VulkanHeaders)

%if %{with tests}
BuildRequires:  libcmocka-devel
%endif

Requires:       hicolor-icon-theme
Requires:       vulkan-loader%{?_isa}

Recommends:     (mangohud(x86-32) if glibc(x86-32))

Suggests:       goverlay

Provides:       bundled(imgui) = %{imgui_ver}

%global _description %{expand:
A modification of the Mesa Vulkan overlay. Including GUI improvements,
temperature reporting, and logging capabilities.

To install GUI front-end:

  # dnf install goverlay}

%description %{_description}


%prep
%autosetup -n %{appname}-master -p1
%setup -qn %{appname}-master -DTa1
%setup -qn %{appname}-master -DTa2

mkdir subprojects/imgui
mv imgui-%{imgui_ver} subprojects/


%build
%meson \
    --wrap-mode=forcefallback \
    -Dinclude_doc=true \
    -Dwith_wayland=enabled \
    -Dwith_xnvctrl=disabled \
    -Dmangoapp=true \
    -Dmangoapp_layer=true \
    -Dmangohudctl=true \
    %if %{with tests}
    -Dtests=enabled \
    %else
    -Dtests=disabled \
    %endif
    %{nil}
%meson_build


%install
%meson_install


%check
# https://github.com/flightlessmango/MangoHud/issues/812
%dnl appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml


%files
%license LICENSE
%doc README.md
%if %{__isa_bits} == 64
%{_bindir}/%{name}*
%{_bindir}/mangoapp
%{_bindir}/mangoplot
%{_datadir}/icons/hicolor/scalable/*/*.svg
%{_docdir}/%{name}/%{appname}.conf.example
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/mangoapp.1*
%{_metainfodir}/*.metainfo.xml
%endif
%{_datadir}/vulkan/implicit_layer.d/*Mango*.json
%{_libdir}/%{name}/libMangoApp.so

%changelog
{{{ git_dir_changelog }}}
