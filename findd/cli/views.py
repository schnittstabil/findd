import logging
from shellescape import quote

from findd.cli.widgets import hr
from findd.cli.widgets import ProgressBarManager


__LOG__ = logging.getLogger(__name__)


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

    def print_duplicates(self, duplicates):
        print(' '.join([quote(afile.relpath) for afile in duplicates]))


class ProcessDuplicatesView(BaseView):
    def __init__(self):
        BaseView.__init__(self, __LOG__.isEnabledFor(logging.INFO))

    def print_subprocess_call(self, args):
        __LOG__.debug(' '.join(args))

    def print_duplicates(self, duplicates):
        if __LOG__.isEnabledFor(logging.INFO):
            print(hr(' processed duplicates '))
            paths = [quote(afile.relpath) for afile in duplicates]
            for path in paths:
                print(path)
            print(hr())
