import sys


if sys.version_info < (3,):
    def u(string):
        return unicode(string) # flake8: noqa
else:
    def u(unicode_string):
        return unicode_string
