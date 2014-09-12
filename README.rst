============================
ZEO server deployment recipe
============================

This package provides for the deployment of simple ZEO servers
constructed using filestorages and demostorages.  Extension to support
additional types of storages should be easy.


Release history
===============

1.1.1 (2014-09-12)
------------------

- Update zc.zk & kazoo to avoid slow restarts.


1.1.0 (2014-04-09)
------------------

- Demostorage: Support base storages using the S3 blob server.
- Move to packagegrinder.
- Update dependencies (use kazoo instead of zc-zookeeper-static).


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
