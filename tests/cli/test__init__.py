from .. import TestCase

from nose.plugins.attrib import attr

from findd.cli import main


@attr('integration')
class Main(TestCase):
    def test_should_throw_exceptions_in_debug_mode(self):
        with self.assertRaises(Exception):
            main(['update', '-vv'])
