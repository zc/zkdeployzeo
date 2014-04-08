import hashlib
import os
import pwd
import zc.metarecipe
import zc.zk


class ZKBaseRecipe(zc.metarecipe.Recipe):

    def __init__(self, buildout, name, options):
        #import pdb; pdb.set_trace()
        super(ZKBaseRecipe, self).__init__(buildout, name, options)

        assert name.endswith('.0'), name # There can be only one.
        self.base_name = str(name[:-2])

        self.user = str(options.get('user', 'zope'))

        self['deployment'] = dict(
            recipe='zc.recipe.deployment',
            name=self.base_name,
            user=self.user,
            )

        self.path = '/' + self.base_name.replace(',', '/')
        self.zk = zc.zk.ZK('zookeeper:2181')
        self.zk_options = self.zk.properties(self.path)
        self.data_dir = '/home/databases' + str(self.path)
        self.blobs = self.zk_options.get('blobs', True)

        self[self.base_name + '-storage'] = dict(
            recipe='zc.zodbrecipes:server',
            deployment='deployment',
            **{
                'zeo.conf': str(zeo_conf % dict(
                    storage=self.storage(),
                    path=self.path,
                    )),
                'shell-script': 'true',
                'zdaemon.conf': zdaemon_conf % self.path,
                })

        self['rc'] = dict(
            recipe='zc.recipe.rhrc',
            deployment='deployment',
            parts=self.base_name + '-storage',
            chkconfig='345 99 10',
            digest=hashlib.sha1(
                repr(sorted(self.zk_options.items()))).hexdigest(),
            **{'process-management': 'true'}
            )


class ZKFileStorageRecipe(ZKBaseRecipe):

    def storage(self):
        self[self.base_name + '-data-directory'] = dict(
            recipe='z3c.recipe.mkdir',
            paths=self.data_dir,
            user=self.user,
            group=self.user,
            **{'remove-on-update': 'true'})

        return zeo_conf_filestorage % dict(
            ddir=self.data_dir,
            zblob=(
                'blob-dir %s/blobs' % str(self.data_dir)
                if self.blobs else ''),
            )


class ZKDemoStorageRecipe(ZKBaseRecipe):

    def storage(self):
        zk_options = self.zk_options

        before = str(zk_options['before'])
        source_path = str(zk_options['path'])
        source_zookeeoper = zk_options.get('zookeeper', 'zookeeper:2181')

        ddir = os.path.join(self.data_dir, before)

        self[self.base_name + '-data-directory'] = dict(
            recipe='z3c.recipe.mkdir',
            paths=ddir,
            user=self.user,
            group=self.user,
            **{'remove-on-update': 'true'})

        #base_zk = zc.zk.ZK(source_zookeeoper)
        #base_options = base_zk.properties(source_path)
        #s3 = base_options.get("s3")
        s3 = False

        base_storage_kind = "zkzeoclient"
        if s3:
            base_storage_kind = "zks3blobclient"
        config = zeo_conf_demostorage % dict(
            ddir=ddir,
            base_storage_kind=base_storage_kind,
            before=before,
            zookeeper=source_zookeeoper,
            source_path=source_path,
            zblob=(
                'blob-dir %s/before.blobs\n'
                '      blob-cache-size 100MB' % ddir
                if self.blobs else ''),
            cblob=(
                'blob-dir %s/changes.blobs' % ddir
                if self.blobs else ''),
            )
        if s3:
            config = "%import zc.s3blobstorage\n" + config
        return config


zeo_conf = """
<zeo>
  address :0
  invalidation-queue-size 10000
  invalidation-age 7200
  transaction-timeout 300
</zeo>
<zookeeper>
  connection zookeeper:2181
  path %(path)s/providers
  monitor-server ${deployment:run-directory}/monitor.sock
</zookeeper>

%%import zc.zlibstorage
%(storage)s
%%import zc.monitorlogstats
<eventlog>
  level INFO
  <counter>
    format %%(name)s %%(message)s
  </counter>
  <logfile>
    path STDOUT
  </logfile>
</eventlog>
"""

zeo_conf_demostorage = """\
%%import zc.beforestorage
%%import zc.zkzeo

<demostorage>
  <before base>
    before %(before)s

    <%(base_storage_kind)s>
      %(zblob)s
      cache-size 100MB
      client before
      read-only true
      read-only-fallback true
      server %(source_path)s
      var %(ddir)s
      zookeeper %(zookeeper)s
    </%(base_storage_kind)s>
  </before>

  <zlibstorage changes>
    <filestorage>
      path %(ddir)s/changes.fs
      %(cblob)s
    </filestorage>
  </zlibstorage>
</demostorage>
"""

zeo_conf_filestorage = """\
<zlibstorage>
  <filestorage>
    path %(ddir)s/Data.fs
    %(zblob)s
  </filestorage>
</zlibstorage>
"""

zdaemon_conf = """
<runner>
  start-test-program ${buildout:bin-directory}/monitorcheck ${deployment:run-directory}/monitor.sock %s/providers
</runner>
"""
