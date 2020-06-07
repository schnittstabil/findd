from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base

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

    def probably_equal(self, afile):
        if afile is None:
            return False

        return (self.size == afile.size and
                self.sha512 == afile.sha512 and
                self.sha384 == afile.sha384 and
                self.sha256 == afile.sha256 and
                self.sha224 == afile.sha224 and
                self.sha1 == afile.sha1 and
                self.md5 == afile.md5)

    def __setitem__(self, k, v):
        setattr(self, k, v)

    def update(self, dict_):
        for key, value in dict_.items():
            self[key] = value


Index(
    'idx_duplicates',
    File.size.desc(),
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
    def __init__(self, session):
        """
        :type session: sqlalchemy.orm.session.Session
        """
        self.session = session

    def update_hashes_if_needed(self):
        duplicate_sizes = self.session \
            .query(File.size) \
            .group_by(File.size) \
            .having(func.count(File.path) > 2)
        files_to_update = self.session.query(File).filter(and_(
            File.size.in_(duplicate_sizes.subquery()),
            or_(
                File.sha512.is_(None),
                File.sha384.is_(None),
                File.sha256.is_(None),
                File.sha224.is_(None),
                File.sha1.is_(None),
                File.md5.is_(None),
            )
        )).order_by(File.size.desc())

        for afile in files_to_update:
            afile.update(hashfile(afile.path))
            self.session.add(afile)
            # commit big files immediately
            if afile.size > 1024 * 1024:
                self.session.commit()
        self.session.commit()

    def find_duplicates(self, limit=-1, skip=0):
        if limit == 0:
            return

        self.update_hashes_if_needed()

        query = self.session.query(File).order_by(
            File.size.desc(),
            File.sha512,
            File.sha384,
            File.sha256,
            File.sha224,
            File.sha1,
            File.md5,
            File.path,
        )
        duplicates = []
        pivot_element = None
        index = 0
        for afile in query:
            if afile.probably_equal(pivot_element):
                duplicates.append(afile)
                continue
            if len(duplicates) > 1 and len(duplicates[skip:]) > 0:
                yield duplicates[skip:]
                index = index + 1
                if index == limit:
                    return
            pivot_element = afile
            duplicates = [afile]

        if len(duplicates) > 1 and len(duplicates[skip:]) > 0:
            yield duplicates[skip:]

    def count(self):
        return self.session.query(func.count(File.path)).scalar()

    def delete(self, db_file):
        self.session.delete(db_file)

    def find_all(self):
        return self.session.query(File)

    def add(self, entity):
        self.session.add(entity)
