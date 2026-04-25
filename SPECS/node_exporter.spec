%global debug_package %{nil}
%global _build_id_links none

# Upstream version — update this to roll a new RPM
%global upstream_version 1.11.1

Name:           node_exporter
Version:        %{upstream_version}
Release:        1%{?dist}
Summary:        Prometheus exporter for hardware and OS metrics
License:        Apache-2.0
URL:            https://github.com/prometheus/node_exporter
# Source tarball downloaded from Prometheus releases (amd64 binary)
Source0:        https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-amd64.tar.gz
Source1:        node_exporter.service
Source2:        node_exporter.sysconfig

# node_exporter is a statically-linked Go binary — no glibc/runtime deps
# Works identically on RHEL/AlmaLinux 8, 9, and 10
BuildArch:      x86_64

Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
node_exporter is a Prometheus exporter that exposes hardware and OS metrics
from *NIX kernels. It is statically linked and runs on RHEL/AlmaLinux 8, 9,
and 10 without modification.

%prep
%setup -q -n node_exporter-%{version}.linux-amd64

%build
# Binary is pre-built upstream; nothing to compile.

%install
install -D -m 0755 node_exporter \
    %{buildroot}%{_bindir}/node_exporter

install -D -m 0644 %{SOURCE1} \
    %{buildroot}%{_unitdir}/node_exporter.service

install -D -m 0640 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/node_exporter

install -d -m 0755 %{buildroot}%{_sharedstatedir}/node_exporter/textfile_collector

%pre
getent group  node_exporter >/dev/null || groupadd -r node_exporter
getent passwd node_exporter >/dev/null || \
    useradd -r -g node_exporter -d /var/lib/node_exporter \
            -s /sbin/nologin \
            -c "Prometheus node_exporter" node_exporter
exit 0

%post
%systemd_post node_exporter.service

%preun
%systemd_preun node_exporter.service

%postun
%systemd_postun_with_restart node_exporter.service

%files
%license LICENSE
%doc NOTICE
%{_bindir}/node_exporter
%{_unitdir}/node_exporter.service
%config(noreplace) %{_sysconfdir}/sysconfig/node_exporter
%dir %attr(0755, node_exporter, node_exporter) %{_sharedstatedir}/node_exporter/textfile_collector

%changelog
* Thu Apr 24 2026 CI Pipeline <ci@example.com> - 1.11.1-1
- Bump to upstream 1.11.1

* Fri Apr 04 2026 CI Pipeline <ci@example.com> - 1.11.0-1
- Bump to upstream 1.11.0

* Sat Oct 25 2025 CI Pipeline <ci@example.com> - 1.10.2-1
- Bump to upstream 1.10.2

* Fri Oct 24 2025 CI Pipeline <ci@example.com> - 1.10.0-1
- Bump to upstream 1.10.0

* Tue Apr 01 2025 CI Pipeline <ci@example.com> - 1.9.1-1
- Bump to upstream 1.9.1
