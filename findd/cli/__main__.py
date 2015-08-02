import errno
import logging
import sys

import findd.cli


if sys.version_info >= (3,):
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def main(args=None):
    try:
        exit_code = findd.cli.main(args)

        # py2: "lost sys.stderr" workaround:
        for flush in [sys.stdout.flush, sys.stderr.flush]:
            try:
                flush()
            except:
                pass

        return exit_code
    except KeyboardInterrupt:
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            raise
    except IOError as err:
        if err.errno == errno.EPIPE:
            return 0
        raise


if __name__ == "__main__":
    sys.exit(main())
