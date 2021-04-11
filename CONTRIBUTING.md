# Contributing

Any change to behavior (including bugfixes) must come with a test.

These tests must fail without the patch, and pass with the patch.

Patches that fail tests or reduce test coverage will be rejected.

In lieu of a formal styleguide, take care to maintain the existing coding style.


## Development Environment

Links:

* [virtualenv issue](https://github.com/stankevich/puppet-python/issues/194)

```bash
# create a virtual environment for development
python3 -m venv .venv

# activate a environment
. .venv/bin/activate

# update pip
pip install --upgrade pip

# install dependencies
python setup.py develop
pip install -r requirements-dev.txt
pip install -r requirements-tests.txt
```


### Testing

#### current python environment

```bash
# run (nose) unittests in tests/
python make.py unittests

# run (nose) integrationtests in tests/
python make.py integrationtests

# run (behave) systemtests in features/
python make.py systemtests
```

#### multiple environments

```bash
# run all tests on all platforms
python make.py test

# run only python3 tests
tox -e py3

# open covery report
xdg-open htmlcov/index.html
```


## Packaging

Links:
* [How to submit a package to PyPI](http://peterdowns.com/posts/first-time-with-pypi.html)
* [Packaging and Distributing Projects](https://packaging.python.org/en/latest/distributing.html)
* [Test PyPI Server](https://wiki.python.org/moin/TestPyPI)
* [Sample Project](https://github.com/pypa/sampleproject)
* [The .pypirc file](https://packaging.python.org/specifications/pypirc)

```bash
# setup .pypirc
cat <<EOF > ~/.pypirc
[distutils]
index-servers=
    pypi
    testpypi

[pypi]
username:
password:

[testpypi]
repository: https://test.pypi.org/legacy/
username:
password:
EOF
chmod 600 ~/.pypirc
editor ~/.pypirc
```

```bash
# run all tests on all platforms
python make.py test

# bump version
editor findd/__about__.py

# create distributions
python make.py dist

tree dist/
# dist/
# ├── findd-…-py3-none-any.whl
# └── findd-….tar.gz

# upload to PyPI Test
twine upload -r testpypi dist/*

# upload to PyPI Live
twine upload -r pypi dist/*
```


## Installing

```bash
# prerequisites
sudo apt-get install python-pip

# local
. .venv/bin/activate
python make.py dist
sudo pip3 install dist/findd-*-py3-none-any.whl --force-reinstall

# PyPI Test
pip3 install -i https://testpypi.python.org/pypi findd

# PyPI Live
pip3 install findd
```
