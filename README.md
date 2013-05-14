# Crate

Manage virtual file repositories with ease.

## Overview

``crate`` is a simple utility that:

* Examines files from a list of sources (typically directories)
* Filters out unwanted files (e.g. if you only wanted the latest versions).
* Stages the filtered files in a temporary directory (typically via symlinks, although 
  this is extensible).
* "Builds" the temporary repository, which usually involves calculating metadata about 
  the available files.
* Migrates the staged repository to a destination location.

The goal of ``crate`` is to make it easy to keep all of your files in their native habitat
(so to speak), and to deploy those files easily according to defined rules without taking
up additional filesystem space.

## Configuration

Repository configuration files live in ``/etc/crate/repos.d`` by default. (This can be 
configured at the command line via the ``-d``/``--config-dir`` option).

Config files are in YAML format.

Here is a simple example:

```yaml
---
driver: rpm
sources:
  - ~/rpmbuild/RPMS/x86_64
  - ~/rpmbuild/RPMS/noarch
destination: /var/www/html/repo
```

In this example, the ``driver`` is ``rpm``, which maps to the ``crate.managers.rpm.RpmManager`` class.

This class has all of the logic necessary to reploy an RPM to an RPM repository. It will 
search through the directories in ``sources`` for any file with the ``.rpm`` suffix. It will
then stage these RPMs (via symlinks) in a temporary directory and run the ``createrepo`` 
utility (which generates the RPM repository metadata). Lastly, it will move the staged files
(as well as all of the repo metadata) to the ``destination``, which is ``/var/www/html/repo``.

In addition to the ``driver``, ``sources``, and ``destination`` directives, you can also specify
``filters``. Filters are a way of winnowing down the files from ``sources`` before deploying into
the configured ``destination``.

Here's an example of filters in action:

```yaml
---
driver: rpm
sources:
  - ~/rpmbuild/RPMS/x86_64
  - ~/rpmbuild/RPMS/noarch
destination: /var/www/html/repo
filters:
  - name: rpm_latest
  - name: rpm_name_regex
    mode: deny
    args:
      - ^foo
      - bar$
```

In this example, we use the ``rpm_latest`` filter to take out all RPMs except the latest. Next, we use
the ``rpm_name_regex`` filter to remove any RPMs that start with ``foo`` or that end in ``bar`` from
consideration.

As you can see, ``filters`` require a ``name`` argument (which maps to a specific ``Filter`` class), and
optionally can take a ``mode`` (which is either ``allow`` or ``deny``) and ``args``. Whether it takes
a ``mode`` or ``args`` is up to the filter (e.g. ``rpm_latest`` does not take ``args`` because it needs
to dynamically compute which RPM packages are the latest).

A full list of filters can be found below in the ``Filters`` section.

## Drivers

Here are the current list of drivers:

* ``file`` - Manage arbitrary files
* ``rpm`` - Manage RPM packages
* ``gem`` - Manage Rubygem packages

## Filters

Here are the current list of filters:

* ``belongs_to`` - Filter based on whether the file is in ``args``.
* ``regex`` - Filter based on whether the file matches any of the regular expressions in ``args``.
* ``rpm_latest`` - Filter away all but the latest RPM packages. Takes no ``args``.
* ``rpm_name`` - Filter based on the RPM name (computed from the RPM package metadata).
* ``rpm_arch`` - Filter based on the RPM architecture (computed from the RPM package metadata).
* ``rpm_name_regex`` - Filter based on RPM name using regular expressions.

