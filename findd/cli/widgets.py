import itertools
import time

from backports.shutil_get_terminal_size import get_terminal_size
from blinker import signal
import progressbar


DEBOUNCE_THRESHOLD = 0.05


def hr(text='', fillchar='*'):
    cols = get_terminal_size((80, 20)).columns
    return text.center(cols, fillchar)


class ProgressBarManager(object):

    def __init__(self):
        self.bars = {}
        self.last_update = {}

    def __enter__(self):
        signal('progress').connect(self.process_progress_signal)
        return self

    def __exit__(self, *_):
        signal('progress').disconnect(self.process_progress_signal)

    def process_progress_signal(self, _, task, state, **kw):
        if state == 'start':
            speed = eta = task == 'hashing'
            maxval = kw['maxval'] if 'maxval' in kw else None
            self.start(task, maxval=maxval, eta=eta, speed=speed)
        elif state == 'update':
            self.update(task, val=kw['val'] if 'val' in kw else None)
        elif state == 'finish':
            self.finish(task)

    def start(self, task, maxval=None, eta=False, speed=False):
        label_width = 16
        widgets = []
        if maxval is None:
            widgets.append(task.ljust(label_width))
            widgets.append(' ')
            widgets.append(progressbar.BouncingBar())
        else:
            widgets.append(task.ljust(label_width - 5))
            widgets.append(' ')
            widgets.append(progressbar.Percentage())
            widgets.append(' ')
            widgets.append(progressbar.Bar())
        if eta and maxval != 0:
            widgets.append(' ')
            widgets.append(progressbar.ETA())
        if speed and maxval != 0:
            widgets.append(' ')
            widgets.append(progressbar.FileTransferSpeed())
        pbar = progressbar.ProgressBar(
            widgets=widgets,
            maxval=maxval if maxval is None or maxval > 0 else 1,
        )
        if maxval is None:
            self.bars[task] = iter(pbar(itertools.repeat(0)))
        else:
            self.bars[task] = pbar.start()
        self.last_update[task] = 0

    def update(self, task, val=None):
        if time.time() - self.last_update[task] < DEBOUNCE_THRESHOLD:
            return  # pragma: no cover
        if val is None:
            self.bars[task].next()
        else:
            self.bars[task].update(val)
        self.last_update[task] = time.time()

    def finish(self, task):
        self.bars[task].finish()
        del self.bars[task]
        del self.last_update[task]
