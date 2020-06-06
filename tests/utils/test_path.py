from os import pathsep
from os.path import basename
from os.path import dirname
from os.path import join
from mock import patch
from mock import Mock
from .. import TestCase

import findd.utils.path as sut


class Parents(TestCase):

    def test_should_work_with_empty_paths(self):
        self.assertEqual(list(sut.parents('')), [''])

    def test_should_work_with_posix_paths(self):
        ps = sut.parents('a/b/c/d')
        prev = next(ps)
        self.assertEqual(prev, 'a/b/c/d')
        if pathsep == '/':
            prev = next(ps)
            self.assertEqual(prev, 'a/b/c')
        for p in ps:
            self.assertEqual(p, dirname(prev))
            prev = p

    def test_should_work_with_nt_paths(self):
        ps = sut.parents('C:\\a\\b\\c\\d')
        prev = next(ps)
        self.assertEqual(prev, 'C:\\a\\b\\c\\d')
        if pathsep == '\\':
            prev = next(ps)
            self.assertEqual(prev, 'C:\\a\\b\\c')
        for p in ps:
            self.assertEqual(p, dirname(prev))
            prev = p


class FilesOfDir(TestCase):

    @patch('findd.utils.path.walk')
    def test_should_work_with_empty_dirs(self, walk):
        walk.return_value = [('virtual', [], [])]
        self.assertEqual(list(sut.files_of_dir('virtual')), [])
        self.assertEqual(len(walk.mock_calls), 1)

    @patch('findd.utils.path.walk')
    @patch('findd.utils.path.stat')
    def test_should_work_with_non_empty_dirs(self, stat, walk):
        walk.return_value = [
            ('virtual', ['dir'], []),
            ('virtual/dir', [], ['123.file'])
        ]
        path123 = 'virtual/dir/123.file'

        files = list(sut.files_of_dir('virtual'))
        self.assertEqual(len(stat.mock_calls), 1)
        self.assertEqual(len(walk.mock_calls), 1)
        stat.assert_called_once_with(path123)
        self.assertEqual(list(map(lambda e: e.path, files)), [path123])

    @patch('findd.utils.path.walk')
    @patch('findd.utils.path.stat')
    def test_should_respect_is_excluded(self, stat, walk):
        def exclude_dotfindd(path):
            return basename(path) == '.findd'
        walk.return_value = [
            ('virtual', ['.findd'], ['root.file']),
        ]
        is_excluded = Mock(side_effect=exclude_dotfindd)
        files = list(sut.files_of_dir('virtual', is_excluded=is_excluded))
        self.assertEqual(len(walk.mock_calls), 1)
        self.assertEqual(len(is_excluded.mock_calls), 2)
        self.assertEqual(len(stat.mock_calls), 1)
        self.assertEqual(walk.return_value[0][1], [])
        paths = list(map(lambda e: e.path, files))
        self.assertEqual(paths, [join('virtual', 'root.file')])
