from mock import patch

from findd.queue import HashTask
from . import TestCase

from findd.services import HashQueue


class HashQueueTest(TestCase):

    @patch('findd.queue.hashfile')
    def test_should_not_raise_on_ioerrors(self, hashfile):
        sut = HashQueue(None)
        sut.append(HashTask('a.txt', 1, {}, False))
        sut.append(HashTask('b.txt', 1, {}, False))
        sut.append(HashTask('c.txt', 1, {}, False))

        hashfile.side_effect = [
            {'md5': 'a'},
            IOError(),
            {'md5': 'c'},
        ]

        sut.process()

        self.assertEqual(len(hashfile.mock_calls), 3)
