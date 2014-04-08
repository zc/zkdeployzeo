import manuel.capture
import manuel.doctest
import manuel.testing
import mock
import zc.zk.testing
import zope.testing.setupstack


def setUp(test):
    zc.zk.testing.setUp(test, '', 'zookeeper:2181')


def setUp(test):
    fauxs = {}
    def add_faux(addr):
        fauxs[addr] = zc.zk.testing.ZooKeeper(addr, zc.zk.testing.Node())
    add_faux("zookeeper:2181")
    add_faux("zk.example.com:2181")

    @zc.zk.testing.side_effect(
        zope.testing.setupstack.context_manager(
            test, mock.patch('kazoo.client.KazooClient')))
    def client(hosts="127.0.0.1:2181", *a, **k):
        return zc.zk.testing.Client(fauxs[hosts], hosts, *a, **k)


def test_suite():
    return manuel.testing.TestSuite(
        manuel.doctest.Manuel() + manuel.capture.Manuel(),
        'README.test',
        setUp=setUp, tearDown=zc.zk.testing.tearDown,
        )
