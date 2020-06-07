"""find duplicate files

Setup script for findd.

usage:
    python setup.py install

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
https://packaging.python.org/en/latest/single_source_version.html
"""

import setuptools

from os import path
from setuptools.command.test import test as TestCommand # NOQA

about = {}
with open(path.join(path.dirname(__file__), "findd", "__about__.py")) as f:
    exec(f.read(), about)

with open('README.rst') as f:
    README_LINES = f.read().splitlines(True)

setuptools.setup(
    name='findd',
    version=about['__version__'],
    description=README_LINES[3].strip(),
    long_description=''.join(README_LINES[5:]).strip(),
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    platforms=['any'],
    keywords='find duplicates cli database-assisted',
    packages=setuptools.find_packages(),
    install_requires=[
        'backports.shutil_get_terminal_size',
        'blinker',
        'inflection',
        'progressbar2',
        'shellescape',
        'sqlalchemy',
        'wheel',
    ],
    entry_points={
        'console_scripts': [
            'findd=findd.cli.__main__:main'
        ],
    },
    python_requires='>=3.4',
)
