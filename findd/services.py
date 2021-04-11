import errno
import logging
import os
from os.path import abspath
from os.path import join
from os.path import relpath

from shlex import quote

from sqlalchemy.orm import Session

from findd import model
from findd.model import FileRegistry, File
from findd.queue import HashQueue, HashTask
from findd.utils.path import files_of_dir
from findd.utils.progress import Progress

__LOG__ = logging.getLogger(__name__)


def dir_aware_file_registry(base_dir: str, file_registry: FileRegistry):
    model_find_all = file_registry.find_all
    model_find_duplicates = file_registry.find_duplicates

    def set_paths(file_: File):
        file_.base_dir = base_dir
        file_.abspath = abspath(join(file_.base_dir, file_.path))
        file_.relpath = relpath(file_.abspath)
        return file_

    def find_all_(*args, **kwargs):
        for file_ in model_find_all(*args, **kwargs):
            yield set_paths(file_)

    def find_duplicates_(*args, **kwargs):
        for dups in model_find_duplicates(*args, **kwargs):
            yield [set_paths(file_) for file_ in dups]

    file_registry.find_all = find_all_
    file_registry.find_duplicates = find_duplicates_
    return file_registry


class Findd(object):

    def __init__(self, base_dir: str, db_session: Session):
        self.base_dir = base_dir
        self.db_session = db_session
        self._file_registry = None

    def init(self):
        progress = Progress('init')
        __LOG__.debug('initializing...')
        progress.start(self, maxval=1)
        model.create_schema(self.db_session.get_bind())
        progress.finish(self)

    def update(self, is_excluded: bool = None, lazy: bool = False):
        update_cmd = _UpdateCommand(
            base_dir=self.base_dir,
            file_registry=self.file_registry,
            is_excluded=is_excluded,
            lazy=lazy
        )
        count = update_cmd.execute()
        self.db_session.commit()
        return count

    def duplicates(self, limit: int = -1, skip: int = 0):
        progress = Progress('find duplicates')
        index = 0
        progress.start(self, maxval=limit if limit > 0 else None)
        for i in self.file_registry.find_duplicates(limit=limit, skip=skip):
            yield i
            index = index + 1
            progress.update(self, val=index)
        progress.finish(self)

    @property
    def file_registry(self):
        if self._file_registry is None:
            self._file_registry = dir_aware_file_registry(
                self.base_dir, model.FileRegistry(self.db_session)
            )
        return self._file_registry


class _UpdateCommand(object):
    def __init__(self, base_dir: str, file_registry: FileRegistry,
                 is_excluded: bool = None, lazy: bool = False):
        assert os.path.exists(base_dir)
        self.base_dir = base_dir
        self.file_registry = file_registry
        self.is_excluded = is_excluded
        self.lazy = lazy
        self.visited_files = []
        self.hash_queue = HashQueue(self.file_registry)

    def _step0_scan_db(self):
        progress = Progress('scanning db')
        __LOG__.debug('scanning db...')
        db_entries_count = self.file_registry.count()
        old_files_deleted = 0
        mtime_changed = 0
        size_changed = 0
        index = 0
        progress.start(self, maxval=db_entries_count)
        for db_file in self.file_registry.find_all():
            index = index + 1
            progress.update(self, val=index)
            abs_path = join(self.base_dir, db_file.path)
            try:
                changed = False
                stat = os.stat(abs_path)
                if db_file.mtime != int(stat.st_mtime):
                    mtime_changed = mtime_changed + 1
                    changed = True
                if db_file.size != stat.st_size:
                    size_changed = size_changed + 1
                    changed = True
                if changed:
                    db_file.mtime = int(stat.st_mtime)
                    db_file.size = stat.st_size
                    self.hash_queue.append(
                        HashTask(abs_path, stat.st_size, db_file, self.lazy)
                    )
                self.visited_files.append(db_file.path)
            except OSError as err:
                if err.errno == errno.ENOENT:
                    __LOG__.debug('deleting %s', quote(db_file.path))
                    self.file_registry.delete(db_file)
                    old_files_deleted = old_files_deleted + 1
                else:
                    raise  # pragma: no cover
        progress.finish(self)
        __LOG__.debug('mtime of %d files changed', mtime_changed)
        __LOG__.debug('size of %d files changed', size_changed)
        __LOG__.debug('%d old files deleted', old_files_deleted)
        return len(self.visited_files)

    def _step1_scan_fs(self):
        progress = Progress('scanning fs')
        __LOG__.debug('scanning %s', quote(self.base_dir))
        new_files_found = 0
        progress.start(self)
        for entry in files_of_dir(self.base_dir, self.is_excluded):
            progress.update(self)
            rel_path = os.path.relpath(entry.path, self.base_dir)
            if rel_path not in self.visited_files:
                new_files_found = new_files_found + 1
                db_file = model.File(
                    path=rel_path,
                    mtime=int(entry.stats.st_mtime),
                    size=entry.stats.st_size,
                )
                self.hash_queue.append(
                    HashTask(entry.path, entry.stats.st_size, db_file,
                             self.lazy)
                )
        progress.finish(self)
        __LOG__.debug('%d new files found', new_files_found)
        return new_files_found

    def execute(self):
        processed_files = self._step0_scan_db() + self._step1_scan_fs()
        self.hash_queue.process()
        self.visited_files = []
        __LOG__.debug('%d files processed', processed_files)
        return processed_files
