from .. import TestCase

from findd.utils.format import sizeof_fmt


class SizeofFmt(TestCase):
    def test_should_format_bytes_correctly(self):
        self.assertEqual(sizeof_fmt(0), '0.0B')
        self.assertEqual(sizeof_fmt(5), '5.0B')

    def test_should_format_gigabytes_correctly(self):
        self.assertEqual(sizeof_fmt(7.8 * 1024 ** 3), '7.8GiB')

    def test_should_format_yotabytes_correctly(self):
        self.assertEqual(sizeof_fmt(42 * 1024 ** 8), '42.0YiB')
