import manuel.capture
import manuel.doctest
import manuel.testing
import zc.zk.testing


def setUp(test):
    zc.zk.testing.setUp(test, '', 'zookeeper:2181')


def test_suite():
    return manuel.testing.TestSuite(
        manuel.doctest.Manuel() + manuel.capture.Manuel(),
        'README.test',
        setUp=setUp, tearDown=zc.zk.testing.tearDown,
        )
