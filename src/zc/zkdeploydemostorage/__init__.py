import hashlib
import os
import pwd
import zc.metarecipe
import zc.zk

class ZKRecipe(
zc.metarecipe.Recipe):

    def __init__(self, buildout, name, options):
        super(ZKRecipe, self).__init__(buildout, name, options)

        assert name.endswith('.0'), name # There can be only one.
        name = name[:-2]

        user = self.user = options.get('user', 'zope')

        self['deployment'] = dict(
            recipe = 'zc.recipe.deployment',
            name=name,
            user=user,
            )

        zk = self.zk = zc.zk.ZK('zookeeper:2181')

        path = '/' + name.replace(',', '/')
        zk_options = zk.properties(path)

        before = zk_options['before']
        source_path = zk_options['path']
        source_zookeeoper = zk_options.get('zookeeper', 'zookeeper:2181')
        blobs = zk_options.get('blobs', True)

        ddir = '/home/databases'+path+'/'+before

        self[name+'data-directory'] = dict(
            recipe = 'z3c.recipe.mkdir',
            paths = ddir,
            user = self.user,
            group = self.user,
            **{'remove-on-update': 'true'})

        self[name+'-storage'] = dict(
            recipe = 'zc.zodbrecipes:server',
            deployment = 'deployment',
            **{
                'zeo.conf': zeo_conf % dict(
                    ddir = ddir,
                    before = before,
                    zookeeper = source_zookeeoper,
                    source_path = source_path,
                    zblob = (
                        'blob-dir %s/before.blobs\nblob-cache-size 100MB' % ddir
                        if blobs else ''),
                    cblob = (
                        'blob-dir %s/changes.blobs' % ddir
                        if blobs else ''),
                    path = path,
                    ),
                'shell-script': 'true',
                'zdaemon.conf': zdaemon_conf % (
                    '${deployment:run-directory}/monitor.sock',
                    path),
            })

        self['rc'] = dict(
            recipe = 'zc.recipe.rhrc',
            deployment = 'deployment',
            parts = name+'-storage',
            chkconfig = '345 99 10',
            digest = hashlib.sha1(repr(sorted(zk_options.items()))).hexdigest(),
            **{'process-management': 'true'}
            )




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

   %%import zc.beforestorage
   %%import zc.zlibstorage

   <demostorage>
     <before base>
        before %(before)s

        <zkzeoclient>
           zookeeper %(zookeeper)s
           client before
           cache_size 100MB
           var %(ddir)s
           server %(source_path)s
           %(zblob)s
        </zkzeoclient>
     </before>

     <zlibstorage changes>
       <filestorage>
         path %(ddir)s/changes.fs
         %(cblob)s
       </filestorage>
     </zlibstorage>
   </demostorage>

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
zdaemon_conf = """
   <runner>
     start-test-program /opt/zkdeploydemostorage/bin/monitorcheck %s %s/providers
   </runner>
"""
