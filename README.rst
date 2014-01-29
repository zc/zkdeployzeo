============================
ZEO server deployment recipe
============================

This package provides for the deployment of simple ZEO servers
constructed using filestorages and demostorages.  Extension to support
additional types of storages should be easy.


Release history
===============

1.1.0 (unreleased)
------------------

- Move to packagegrinder.
- Update dependencies.


1.0.2 (2013-02-28)
------------------

- Fix permissions issue in generated RPMs.
- Move to buildout 2.


1.0.1 (2013-02-28)
------------------

For demo storages, we need to use a read-only connection to the base
storage; we're not going to write there, and it may be a read-only
replica.


1.0.0 (2013-01-15)
------------------

Initial release.
