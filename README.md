# node_exporter RPM – RHEL / AlmaLinux 8, 9, 10

Automated CI/CD pipeline that builds **node_exporter** RPMs for amd64 targeting RHEL/AlmaLinux 8, 9, and 10.

## Why this repo?

Prometheus ships node_exporter as a statically-linked Go binary — no runtime dependencies — making a single spec file usable across all RHEL family majors. This repo automates tracking upstream releases and publishing distro-tagged packages.

## Packages produced

| RPM file | Target |
|----------|--------|
| `node_exporter-<ver>-<rel>.el8.x86_64.rpm` | RHEL 8 / AlmaLinux 8 |
| `node_exporter-<ver>-<rel>.el9.x86_64.rpm` | RHEL 9 / AlmaLinux 9 |
| `node_exporter-<ver>-<rel>.el10.x86_64.rpm` | RHEL 10 / AlmaLinux 10 |

All three packages ship the identical binary; the `dist` tag is the only difference.

## Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `build-rpm.yml` | push to `main`, any `v*` tag, manual | Build RPMs; publish a GitHub Release on tags |
| `check-upstream.yml` | daily 06:00 UTC, manual | Detect new upstream releases, bump spec, push tag |

## Versioning & tagging convention

| Tag | Meaning |
|-----|---------|
| `v1.11.1` | upstream 1.11.1, RPM release 1 |
| `v1.11.1-2` | upstream 1.11.1, RPM release 2 (spec-only fix) |

Pushing a tag matching `v*` triggers the full build + release job.

## Install

Download the appropriate RPM from the [Releases](../../releases) page.

```bash
# Example – RHEL/AlmaLinux 9
sudo rpm -ivh node_exporter-1.11.1-1.el9.x86_64.rpm
sudo systemctl daemon-reload
sudo systemctl enable --now node_exporter
```

Verify:

```bash
curl -s http://localhost:9100/metrics | head
```

## Configuration

Edit `/etc/sysconfig/node_exporter` to pass extra flags:

```bash
NODE_EXPORTER_OPTS="--collector.textfile.directory=/var/lib/node_exporter/textfile_collector \
                    --web.listen-address=:9100"
sudo systemctl restart node_exporter
```

## Local build

Requires `rpmbuild` / `rpmdevtools` and `wget`.

```bash
# Build for el9 (default)
make

# Build for a specific distro tag
make DIST=el8
make DIST=el10

# Build a specific upstream version
sed -i 's/^%global upstream_version .*/\%global upstream_version 1.11.1/' SPECS/node_exporter.spec
make
```

## Manual trigger for a specific version

Go to **Actions → Build node_exporter RPM → Run workflow**, enter the desired upstream version (e.g. `1.11.1`), and click **Run workflow**.

## Repository structure

```
.
├── .github/
│   └── workflows/
│       ├── build-rpm.yml        # Build + release pipeline
│       └── check-upstream.yml   # Daily upstream version check
├── SOURCES/
│   ├── node_exporter.service    # systemd unit
│   └── node_exporter.sysconfig  # /etc/sysconfig defaults
├── SPECS/
│   └── node_exporter.spec       # RPM spec (distro-agnostic)
└── Makefile                     # Local build helper
```
