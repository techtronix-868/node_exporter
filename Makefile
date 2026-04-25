UPSTREAM_VERSION := $(shell grep -E '^%global upstream_version' SPECS/node_exporter.spec | awk '{print $$3}')
RPM_RELEASE      := 1
DIST             ?= el9
TARBALL          := node_exporter-$(UPSTREAM_VERSION).linux-amd64.tar.gz
TARBALL_URL      := https://github.com/prometheus/node_exporter/releases/download/v$(UPSTREAM_VERSION)/$(TARBALL)

.PHONY: all setup download build clean

all: setup download build

setup:
	rpmdev-setuptree
	cp SOURCES/* ~/rpmbuild/SOURCES/
	cp SPECS/node_exporter.spec ~/rpmbuild/SPECS/

download:
	@if [ ! -f SOURCES/$(TARBALL) ]; then \
	    echo "Downloading $(TARBALL_URL)"; \
	    wget -q --show-progress -P SOURCES/ $(TARBALL_URL); \
	fi
	cp SOURCES/$(TARBALL) ~/rpmbuild/SOURCES/

build:
	rpmbuild -bb --define "dist .$(DIST)" ~/rpmbuild/SPECS/node_exporter.spec

clean:
	rm -f SOURCES/$(TARBALL)
	rm -rf ~/rpmbuild/RPMS/x86_64/node_exporter-*.rpm
