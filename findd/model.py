from sqlalchemy import Column, desc
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased, Query
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.operators import is_

from findd.utils.crypto import hashfile

BASE = declarative_base()


class File(BASE):
    __tablename__ = 'file'

    path = Column(String, primary_key=True)
    mtime = Column(Integer)
    size = Column(Integer)
    md5 = Column(String(32))
    sha1 = Column(String(40))
    sha224 = Column(String(56))
    sha256 = Column(String(64))
    sha384 = Column(String(96))
    sha512 = Column(String(128))

    def probably_equal(self, file_):
        if file_ is None:
            return False

        return (self.size == file_.size and
                self.sha512 == file_.sha512 and
                self.sha384 == file_.sha384 and
                self.sha256 == file_.sha256 and
                self.sha224 == file_.sha224 and
                self.sha1 == file_.sha1 and
                self.md5 == file_.md5)

    def __setitem__(self, k, v):
        setattr(self, k, v)

    def update(self, dict_):
        for key, value in dict_.items():
            self[key] = value


Index(
    'idx_duplicates',
    desc(File.size),
    File.sha512,
    File.sha384,
    File.sha256,
    File.sha224,
    File.sha1,
    File.md5,
    File.path,  # covering idx
    File.mtime,  # covering idx
    unique=True,  # covering idx
)


def create_schema(connectable):
    BASE.metadata.create_all(connectable)


class FileRegistry(object):
    def __init__(self, session: Session):
        self.session = session

    def update_hashes_if_needed(self):
        file_alias = aliased(File)

        files_to_update = self.session. \
            query(File). \
            distinct(). \
            join(file_alias, and_(File.path != file_alias.path,
                                  File.size == file_alias.size,
                                  )).\
            filter(or_(is_(File.sha512, None),
                       is_(File.sha384, None),
                       is_(File.sha256, None),
                       is_(File.sha224, None),
                       is_(File.sha1, None),
                       is_(File.md5, None),
                       ))

        for a_file in files_to_update:
            a_file.update(hashfile(a_file.path))
            self.session.add(a_file)
            # commit big files immediately
            if a_file.size > 1024 * 1024:
                self.commit()  # pragma: no cover
        self.commit()

    def find_duplicates(self, limit=-1, skip=0):
        if limit == 0:
            return

        self.update_hashes_if_needed()

        file_alias = aliased(File)
        query = self.session. \
            query(File). \
            distinct(). \
            join(file_alias, and_(File.path != file_alias.path,
                                  File.size == file_alias.size,
                                  File.sha512 == file_alias.sha512,
                                  File.sha384 == file_alias.sha384,
                                  File.sha256 == file_alias.sha256,
                                  File.sha224 == file_alias.sha224,
                                  File.sha1 == file_alias.sha1,
                                  File.md5 == file_alias.md5,
                                  )).\
            order_by(desc(File.size))

        duplicates = []
        pivot_element = None
        index = 0
        for file_ in query:
            if file_.probably_equal(pivot_element):
                duplicates.append(file_)
                continue
            if len(duplicates) > 1 and len(duplicates[skip:]) > 0:
                yield duplicates[skip:]
                index = index + 1
                if index == limit:
                    return
            pivot_element = file_
            duplicates = [file_]

        if len(duplicates) > 1 and len(duplicates[skip:]) > 0:
            yield duplicates[skip:]

    def count(self):
        return self.session.query(func.count(File.path)).scalar()

    def delete(self, db_file: File):
        self.session.delete(db_file)

    def find_all(self) -> Query:
        return self.session.query(File)

    def add(self, entity) -> None:
        self.session.add(entity)

    def commit(self) -> None:
        self.session.commit()
