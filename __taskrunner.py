import argparse
import errno
import functools
import glob
import os
import shutil
import subprocess
import sys


ARG_PARSER = argparse.ArgumentParser()
TASKS = ARG_PARSER.add_subparsers()


def task(func=None, **task_args):
    if func is None:
        return functools.partial(task, **task_args)
    task_parser = TASKS.add_parser(func.__name__, **task_args)
    task_parser.set_defaults(func=func)
    return func


def run(args):
    if type(args) is str:
        args = args.split()
    try:
        return_code = subprocess.call(args)
        if return_code != 0:
            sys.exit(return_code)
    except OSError as err:
        if err.errno == errno.ENOENT:
            print('command not found: ' + ' '.join(args))
            sys.exit(1)
        else:
            raise


def rimraf(*patterns):
    for pattern in patterns:
        for path_ in glob.glob(pattern):
            try:
                os.remove(path_)
            except OSError as err:
                if err.errno == errno.EISDIR:
                    shutil.rmtree(path_)


def main():
    opts = ARG_PARSER.parse_args()
    if hasattr(opts, 'func'):
        opts.func()
    else:
        ARG_PARSER.print_help()
