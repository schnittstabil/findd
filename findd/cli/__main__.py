import errno
import logging
import signal
import sys

import findd.cli

signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def main(args=None):
    try:
        return findd.cli.main(args)
    except KeyboardInterrupt:
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            raise
    except IOError as err:
        if err.errno == errno.EPIPE:
            return 0
        raise


if __name__ == "__main__":
    sys.exit(main())
