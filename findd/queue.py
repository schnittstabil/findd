import logging
from shlex import quote
from typing import TypeVar, Generic

from findd.model import File, FileRegistry
from findd.utils.crypto import hashfile
from findd.utils.format import sizeof_fmt

__LOG__ = logging.getLogger(__name__)

from findd.utils.progress import Progress


class Task(object):
    def __init__(self, costs: int):
        self.costs = costs

    def execute(self):
        pass  # pragma: no cover


class HashTask(Task):
    def __init__(self, file_path: str, file_size: int, model: File,
                 lazy: bool):
        super(HashTask, self).__init__(file_size)
        self.file_size = file_size
        self.file_path = file_path
        self.model = model
        self.lazy = lazy

    def execute(self):
        if self.lazy:
            return

        __LOG__.debug('hashing %s (%s)...',
                      quote(self.file_path),
                      sizeof_fmt(self.file_size))

        try:
            self.model.update(hashfile(self.file_path))
            __LOG__.debug('update of %s succeeded', self.file_path)
        except Exception as err:
            __LOG__.exception('hashing of %s failed: %s', self.file_path, err)
            raise


QueueTask = TypeVar('QueueTask', bound=Task)


class Queue(Generic[QueueTask]):
    def __init__(self, progress: Progress = None):
        self.__progress = progress
        self._todo = []
        self.processed_tasks = 0

    def costs(self):
        return sum([task.costs for task in self._todo])

    def append(self, task: QueueTask):
        self._todo.append(task)

    def _process_start(self):
        pass  # pragma: no cover

    def _task_succeeded(self, task: QueueTask):
        pass  # pragma: no cover

    def _task_failed(self, task: QueueTask):
        pass  # pragma: no cover

    def _process_finish(self):
        pass  # pragma: no cover

    @staticmethod
    def process_task(task: QueueTask):
        task.execute()

    def process(self):
        self.processed_tasks = 0
        processed = 0
        self._process_start()
        self.__progress.start(self, maxval=self.costs())
        for task in self._todo:
            try:
                self.process_task(task)
                self._task_succeeded(task)
            except Exception as err:
                __LOG__.exception('task failed: %s', err)
                self._task_failed(task)
            processed = processed + task.costs
            self.__progress.update(self, val=processed)
            self.processed_tasks = self.processed_tasks + 1
        self.__progress.finish(self)
        self._process_finish()


class HashQueue(Queue[HashTask]):

    def __init__(self, file_registry: FileRegistry):
        super(HashQueue, self).__init__(Progress('hashing'))
        self.file_registry = file_registry

    def _process_start(self):
        __LOG__.debug(
            'hashing %d files (%s)',
            len(self._todo),
            sizeof_fmt(self.costs())
        )

    def _task_succeeded(self, task: HashTask):
        if self.file_registry:
            self.file_registry.add(task.model)
            if self.processed_tasks % 10 == 0 or task.model.size > 1024 * 1024:
                self.file_registry.commit()

    def _process_finish(self):
        if self.file_registry:
            self.file_registry.commit()
        __LOG__.debug('%d files hashed', len(self._todo))
