from collections import namedtuple
from os import stat
from os import walk
from os.path import dirname
from os.path import join


FileEntry = namedtuple('File', 'path stats')


def parents(directory):
    last = None
    while last != directory:
        yield directory
        last = directory
        directory = dirname(directory)


def files_of_dir(directory, is_excluded=None):
    for root, dirs, files in walk(directory):
        if is_excluded is not None:
            for names in [dirs, files]:
                for name in names:
                    if is_excluded(join(root, name)):
                        names.remove(name)

        for fname in files:
            path = join(root, fname)
            yield FileEntry(path, stat(path))
