import unittest
import manuel.capture
import manuel.doctest
import manuel.testing
import re
import zc.zk.testing
import zope.testing.renormalizing

def setUp(test):
    zc.zk.testing.setUp(test, '', 'zookeeper:2181')

def test_suite():
    return unittest.TestSuite((
        manuel.testing.TestSuite(
            manuel.doctest.Manuel() + manuel.capture.Manuel(),
            'README.test',
            setUp=setUp, tearDown=zc.zk.testing.tearDown,
            ),
        ))
