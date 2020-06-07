import os
import subprocess

from findd.cli import context
from findd.cli.views import InitView
from findd.cli.views import ListDuplicatesView
from findd.cli.views import ProcessDuplicatesView
from findd.cli.views import UpdateView


def init(_):
    with InitView():
        ctx = context.create_from_base_dir(base_dir=os.getcwd())
        ctx.assert_findd_dir_does_not_exists()
        os.makedirs(ctx.findd_dir)
        ctx.findd().init()


def update(opts):
    with UpdateView():
        ctx = context.create_from_base_dir()
        ctx.assert_findd_dir_exists()
        ctx.findd().update(is_excluded=ctx.is_excluded, lazy=opts.lazy)


def list_duplicates(opts):
    with ListDuplicatesView() as view:
        ctx = context.create_from_base_dir()
        ctx.assert_findd_dir_exists()
        for dups in ctx.findd().duplicates(limit=opts.limit, skip=opts.skip):
            view.print_duplicates(dups)


def process_duplicates(opts):
    with ProcessDuplicatesView() as view:
        ctx = context.create_from_base_dir()
        ctx.assert_findd_dir_exists()
        for dups in ctx.findd().duplicates(limit=opts.limit, skip=opts.skip):
            paths = [afile.relpath for afile in dups]
            call_args = [opts.cmd] + opts.args + paths
            view.print_subprocess_call(call_args)
            subprocess.call(call_args)
            view.print_duplicates(dups)
