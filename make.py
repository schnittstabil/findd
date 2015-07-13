#!/usr/bin/env python

import os
from __taskrunner import main
from __taskrunner import rimraf
from __taskrunner import run
from __taskrunner import task


@task(help='lint source and test files')
def lint():
    run('flake8 findd tests')


@task(help='run all tests on all platforms')
def test():
    lint()
    coverage_clean()
    run('tox')
    coverage_report()


@task(help='run tests used by tox')
def tox_tests():
    run('coverage run -m nose --with-spec --spec-color')
    run('coverage run -m behave')


def coverage_clean():
    rimraf('.coverage')
    rimraf('.coverage.*')
    rimraf('htmlcov')
    run('coverage erase')


def coverage_report():
    run('coverage combine')
    run('coverage html')
    run('coverage report')


@task(help='run unittests on current platform')
def unittests():
    coverage_clean()
    run('coverage run -m nose --with-spec --spec-color --attr=!integration')
    coverage_report()


@task(help='run integrationtests on current platform')
def integrationtests():
    coverage_clean()
    run('coverage run -m nose --with-spec --spec-color --attr=integration')
    coverage_report()


@task(help='run systemtests on current platform')
def systemtests():
    coverage_clean()
    run('coverage run -m behave')
    coverage_report()


@task(help='determine overall test coverage of current platform')
def coverage():
    coverage_clean()
    tox_tests()
    coverage_report()


def project_clean():
    rimraf('build')
    rimraf('dist')
    rimraf('temp')
    rimraf('*.egg')
    rimraf('*.egg-info/')

    rimraf('*.pyc')
    rimraf('__pycache__')
    for path_ in ['findd', 'tests']:
        for root, dirs, files in os.walk(path_):
            rimraf(os.path.join(root, '*.pyc'))
            if '__pycache__' in dirs:
                rimraf(os.path.join(root, '__pycache__'))
                dirs.remove('__pycache__')


@task(help='remove files created by ' + os.path.basename(__file__))
def clean():
    project_clean()
    coverage_clean()


@task(help='create source and wheel distribution')
def dist():
    project_clean()
    run('python setup.py sdist bdist_wheel')

if __name__ == "__main__":
    main()
