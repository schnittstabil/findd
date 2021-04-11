import ast
import errno
import importlib

import os
import shutil
import subprocess

from behave import given, when, then
from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import is_not
from hamcrest import matches_regexp
from hamcrest import not_none

TEMP_DIR = os.path.join(os.getcwd(), 'temp')
FINDD = os.path.join(os.getcwd(), 'findd', 'cli', '__main__.py')


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def convert_path(path):
    return os.path.join(*path.split('/'))


@when('I import the {name} package')
def step_impl(context, name):
    if not hasattr(context, 'imported'):
        context.imported = {}
    context.imported[name] = importlib.import_module(name)


@then('the {name} package {attr} value exists')
def step_impl(context, name, attr):
    assert_that(hasattr(context.imported[name], attr), equal_to(True))


@given('an uninitialized directory')
def step_impl(context):
    base_dir = os.path.join(TEMP_DIR, 'uninitialized')
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(base_dir)
    os.chdir(base_dir)
    context.base_dir = base_dir


@given('an initialized directory')
def step_impl(context):
    base_dir = os.path.join(TEMP_DIR, 'initialized')
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(base_dir)
    os.chdir(base_dir)
    import findd.cli.commands
    findd.cli.commands.init(None)
    context.base_dir = base_dir


@when('containing files')
@given('containing files')
def step_impl(context):
    for row in context.table:
        file_path = convert_path(row['path'])
        parent_dir = os.path.dirname(os.path.abspath(file_path))
        mkdir_p(parent_dir)
        with open(file_path, 'w') as text_file:
            text_file.write(row['content'])
        if row.get('mtime_offset', None) is not None:
            mtime_offset = ast.literal_eval(row['mtime_offset'])
            atime = os.path.getatime(file_path)
            mtime = os.path.getmtime(file_path) + mtime_offset
            os.utime(file_path, (atime, mtime))


@when('I run {args} in a shell')
def step_impl(context, args):
    args = ast.literal_eval(args)
    process = subprocess.Popen(
        args.format(FINDD=FINDD),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True,
    )
    (stdoutdata, stderrdata) = process.communicate()

    stdoutdata = stdoutdata.decode('utf-8')
    stderrdata = stderrdata.decode('utf-8')

    context.stdout_capture_ = stdoutdata
    context.stderr_capture_ = stderrdata
    context.exit_code = process.returncode


def run_findd(context, args, cwd=None):
    args = ast.literal_eval(args)
    if cwd is not None:
        cwd = ast.literal_eval(cwd)

        if cwd is not None:
            os.chdir(cwd)

    import findd.cli
    findd.cli.widgets.DEBOUNCE_THRESHOLD = 0
    context.exit_code = findd.cli.main(args)


when('I run findd with {args} in {cwd}')(run_findd)


when('I run findd with {args}')(run_findd)


@when('I delete the files {files}')
def step_impl(context, files):
    paths = map(convert_path, ast.literal_eval(files))
    for p in paths:
        os.remove(p)


@when('I change content of file {file_path} to {content}')
def step_impl(context, file_path, content):
    file_path = convert_path(ast.literal_eval(file_path))
    content = ast.literal_eval(content)
    with open(file_path, 'w') as text_file:
        text_file.write(content)


@then('the file contents of {path} matches {expr}')
def step_impl(context, path, expr):
    file_path = convert_path(ast.literal_eval(path))
    pattern = ast.literal_eval(expr)
    with open(file_path, 'r') as text_file:
        actual = text_file.read()
    assert_that(actual, matches_regexp(pattern))


@then('the {attr} matches {expr}')
def step_impl(context, attr, expr):
    actual = getattr(context, attr)
    if hasattr(actual, 'getvalue'):
        actual = actual.getvalue()
    pattern = ast.literal_eval(expr)
    assert_that(actual, matches_regexp(pattern))


@then('the {attr} is non-zero')
def step_impl(context, attr):
    actual = getattr(context, attr)
    assert_that(actual, not_none())
    assert_that(actual, is_not(equal_to(0)))


@then('the {attr} is zero')
def step_impl(context, attr):
    actual = getattr(context, attr)
    assert_that(actual, equal_to(0))
