import sys


if sys.version_info < (3,):
    import codecs

    def u(string):
        return codecs.decode(string, 'utf8', 'replace')

    def s(unicode_string):
        return codecs.encode(unicode_string, 'utf8', 'replace')

else:
    def u(unicode_string):
        return unicode_string

    def s(unicode_string):
        return unicode_string
