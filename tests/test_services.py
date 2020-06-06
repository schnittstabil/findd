from mock import patch
from . import TestCase

from findd.services import HashQueue


class HashQueueTest(TestCase):

    @patch('findd.services.hashfile')
    def test_should_not_raise_on_ioerrors(self, hashfile):
        sut = HashQueue()
        sut.append('a.txt', 1)
        sut.append('b.txt', 1)
        sut.append('c.txt', 1)

        hashfile.side_effect = [
            {'md5': 'a'},
            IOError(),
            {'md5': 'c'},
        ]

        results = sut.process()

        self.assertEqual(len(hashfile.mock_calls), 3)
        self.assertEqual(results, [
            {'md5': 'a'},
            {'md5': 'c'},
        ])

        self.assertEqual(len(sut.errors), 1)
        self.assertIsInstance(sut.errors[0], IOError)
