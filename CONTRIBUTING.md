Contributing
============

Any change to behavior (including bugfixes) must come with a test.

These tests must fail without the patch, and pass with the patch.

Patches that fail tests or reduce test coverage will be rejected.

In lieu of a formal styleguide, take care to maintain the existing coding style.


Development Environment
=======================

Links:

* [virtualenv issue](https://github.com/stankevich/puppet-python/issues/194)

```bash
# prerequisites
$ sudo apt-get install python-virtualenv python-dev python3-dev

# create a virtual environments for development
findd$ virtualenv -p `which python2` .virtualenvs/dev2
findd$ virtualenv -p `which python3` .virtualenvs/dev3

# activate a environment
findd$ . .virtualenvs/dev3/bin/activate

# install dependencies
(dev3)findd$ python setup.py develop
(dev3)findd$ pip install -r requirements-dev.txt
(dev3)findd$ pip install -r requirements-tests.txt
```


Testing
-------

### current python environment

```bash
# run (nose) unittests in tests/
(dev3)findd$ python make.py unittests

# run (nose) integrationtests in tests/
(dev3)findd$ python make.py integrationtests

# run (behave) systemtests in features/
(dev3)findd$ python make.py systemtests
```

### multiple environments

```bash
# run all tests on all platforms
(dev3)findd$ python make.py test

# run only python2.7 tests
(dev3)findd$ tox -e py27

# run only python3.4 tests
(dev3)findd$ tox -e py34


# open covery report
xdg-open htmlcov/index.html
```


Sublime
-------

Install Packages:

1. `STRG`+`SHIFT`+`P`
2. `Package Control: Install Package`

Packages:

* `Python Flake8 Lint`


Packaging
=========

Links:
* [How to submit a package to PyPI](http://peterdowns.com/posts/first-time-with-pypi.html)
* [Packaging and Distributing Projects](https://packaging.python.org/en/latest/distributing.html)
* [Test PyPI Server](https://wiki.python.org/moin/TestPyPI)
* [Sample Project](https://github.com/pypa/sampleproject)

```bash
# run all tests on all platforms
(dev3)findd$ python make.py test

# edit findd/__about__.py

# create distributions
(dev3)findd$ python make.py dist

(dev3)findd$ tree dist/
dist/
├── findd-…-py2.py3-none-any.whl
└── findd-….tar.gz

# upload to PyPI Test
(dev3)findd$ twine upload -r pypitest dist/*

# upload to PyPI Live
(dev3)findd$ twine upload -r pypi dist/*
```


Installing
==========

```bash
# prerequisites
$ sudo apt-get install python-pip

# local
$ sudo pip install <PATH_TO>/dist/findd-*-py2.py3-none-any.whl

# PyPI Test
$ pip install -i https://testpypi.python.org/pypi findd

# PyPI Live
$ pip install findd
```
