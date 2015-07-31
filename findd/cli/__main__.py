import errno
import sys

import findd.cli


def main(args=None):
    try:
        return findd.cli.main(args)
    except KeyboardInterrupt:
        pass
    except Exception as err:
        if sys.version_info < (3,):
            if not isinstance(err, IOError) or err.errno != errno.EPIPE:
                raise
        else:
            if not isinstance(err, BrokenPipeError): # flake8: noqa
                raise
    finally:
        for stream in [sys.stdout, sys.stderr]:
            for f in [stream.flush, stream.close]:
                try:
                    f()
                except:
                    pass


if __name__ == "__main__":
    sys.exit(main())
