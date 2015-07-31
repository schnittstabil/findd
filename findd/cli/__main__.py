import errno
import logging
import sys

from findd.cli import context
from findd.cli.parser import build as build_parser


def main(args=None):
    parser = build_parser()
    opts = parser.parse_args(args)
    context.configure_logging(opts.verbosity)
    try:
        if hasattr(opts, 'func'):
            opts.func(opts)
        else:
            parser.print_help()
        sys.exit(0)
    except Exception as err:
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            raise
        err_module = getattr(err, '__module__', '')
        if err_module.split('.')[0] != 'findd':
            raise  # pragma: no cover
        logging.error(err)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    def ignore_broken_pipe(f):
        try:
            f()
        except IOError as err:
            if err.errno != errno.EPIPE:
                raise

    try:
        ignore_broken_pipe(main)
    except KeyboardInterrupt:
        pass
    finally:
        ignore_broken_pipe(sys.stdout.flush)
        ignore_broken_pipe(sys.stdout.close)
        ignore_broken_pipe(sys.stderr.flush)
        ignore_broken_pipe(sys.stderr.close)
