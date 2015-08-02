import os
import logging

import sqlalchemy

from findd.services import Findd
from findd.utils.path import parents


__LOG__ = logging.getLogger(__name__)
DEBUG_MORE = 5


class ContextException(Exception):
    pass


class Context(object):

    def __init__(self, base_dir, findd_dir, db_url):
        assert base_dir is not None
        assert findd_dir is not None
        assert db_url is not None

        assert os.path.exists(base_dir)

        self.base_dir = base_dir
        self.findd_dir = findd_dir
        self.db_url = db_url

    def assert_findd_dir_does_not_exists(self):
        if os.path.exists(self.findd_dir):
            raise ContextException('.findd directory already exists')

    def assert_findd_dir_exists(self):
        if not os.path.exists(self.findd_dir):
            raise ContextException('.findd directory not found')

    def db_engine(self):
        echo = __LOG__.isEnabledFor(DEBUG_MORE)
        return sqlalchemy.create_engine(self.db_url, echo=echo)

    def db_sessionmaker(self):
        return sqlalchemy.orm.sessionmaker(bind=self.db_engine())

    def db_session(self):
        return self.db_sessionmaker()()

    def findd(self):
        return Findd(base_dir=self.base_dir, db_session=self.db_session())

    @property
    def is_excluded(self):
        return lambda path: os.path.basename(path) == '.findd'


def search_base_dir(start_dir=None):
    if start_dir is None:
        start_dir = os.getcwd()

    for path in parents(start_dir):
        if os.path.exists(os.path.join(path, '.findd')):
            return path

    return os.getcwd()


def create_from_base_dir(base_dir=None):
    if base_dir is None:
        base_dir = search_base_dir()

    findd_dir = os.path.join(base_dir, '.findd')
    db_path = os.path.join(findd_dir, 'findd.sqlite3')
    db_url = 'sqlite:///%s' % db_path

    return Context(
        base_dir=base_dir,
        findd_dir=findd_dir,
        db_url=db_url,
    )


def configure_logging(verbosity):
    levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
        DEBUG_MORE,
    ]
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=levels[2 + max(min(verbosity, 3), -2)]
    )
    logging.addLevelName(DEBUG_MORE, 'DEBUG')
