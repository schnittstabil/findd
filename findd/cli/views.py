import logging
from os.path import join
from os.path import normpath
from os.path import relpath
from shellescape import quote

from findd.cli.widgets import hr
from findd.cli.widgets import ProgressBarManager


__LOG__ = logging.getLogger(__name__)


def _format_path(base_dir, path):
    return quote(relpath(normpath(join(base_dir, path))))


def _format_duplicates(base_dir, duplicates):
    return [_format_path(base_dir, afile.path) for afile in duplicates]


class BaseView(object):
    def __init__(self, show_progressbars):
        self.pbm = ProgressBarManager() if show_progressbars else None

    def __enter__(self):
        if self.pbm is not None:
            self.pbm.__enter__()
        return self

    def __exit__(self, *args):
        if self.pbm is not None:
            self.pbm.__exit__(*args)


class InitView(BaseView):
    def __init__(self):
        BaseView.__init__(self, __LOG__.isEnabledFor(logging.INFO))


class UpdateView(BaseView):
    def __init__(self):
        BaseView.__init__(self, __LOG__.isEnabledFor(logging.INFO))


class ListDuplicatesView(BaseView):
    def __init__(self):
        BaseView.__init__(self, False)

    def print_duplicates(self, base_dir, duplicates):
        print(' '.join(_format_duplicates(base_dir, duplicates)))


class ProcessDuplicatesView(BaseView):
    def __init__(self):
        BaseView.__init__(self, __LOG__.isEnabledFor(logging.INFO))

    def print_subprocess_call(self, args):
        __LOG__.debug(' '.join(args))

    def print_duplicates(self, base_dir, duplicates):
        if __LOG__.isEnabledFor(logging.INFO):
            print(hr(' processed duplicates '))
            for path in _format_duplicates(base_dir, duplicates):
                print(path)
            print(hr())
