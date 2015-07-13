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
