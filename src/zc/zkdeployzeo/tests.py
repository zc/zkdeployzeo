import manuel.capture
import manuel.doctest
import manuel.testing
import mock
import unittest
import zc.zk.testing
import zope.testing.setupstack


def setUp(test):
    zc.zk.testing.setUp(test, '', 'zookeeper:2181')


def setUp2(test):
    faux1 = zc.zk.testing.ZooKeeper(
        "zookeeper:2181", zc.zk.testing.Node())
    faux2 = zc.zk.testing.ZooKeeper(
        "zookeeper.example.com:2181", zc.zk.testing.Node())

    @zc.zk.testing.side_effect(
        zope.testing.setupstack.context_manager(
            test, mock.patch('kazoo.client.KazooClient')))
    def client(*a, **k):
        print a, k
        return zc.zk.testing.Client(faux1, *a, **k)



def test_suite():
    return unittest.TestSuite([
        manuel.testing.TestSuite(
            manuel.doctest.Manuel() + manuel.capture.Manuel(),
            'README.test',
            setUp=setUp, tearDown=zc.zk.testing.tearDown,
            ),
        manuel.testing.TestSuite(
            manuel.doctest.Manuel() + manuel.capture.Manuel(),
            'two.txt',
            setUp=setUp2, tearDown=zc.zk.testing.tearDown,
            ),
        ])
