from gettext import gettext
import logging

from findd.cli import context
from findd.cli.parser import build as build_parser


def main(args=None):
    parser = build_parser()
    try:
        opts = parser.parse_args(args)
        if not hasattr(opts, 'func'):
            parser.error(gettext('too few arguments'))
    except SystemExit as err:
        return 2 if err.code is None else err.code

    context.configure_logging(opts.verbosity)

    try:
        opts.func(opts)
        return 0
    except Exception as err:
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            raise

        err_module = getattr(err, '__module__', '')
        if err_module.split('.')[0] == 'findd':
            logging.error(err)
            return 1

        raise  # pragma: no cover
