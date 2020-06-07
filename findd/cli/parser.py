from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import os

from findd import __about__
from findd.cli import commands


def build():
    builder = ParserBuilder(
        prog='findd',
        homepage=__about__.__url__,
        bugs_url=__about__.__bugs_url__,
    )
    builder.add_version_argument(__about__.__version__)
    builder.add_init_parser()
    builder.add_update_parser()
    builder.add_list_parser()
    builder.add_run_parser()
    return builder.build()


class FinddArgumentParser(ArgumentParser):
    def parse_known_args(self, args=None, namespace=None):
        args, argv = ArgumentParser.parse_known_args(
            self,
            args=args,
            namespace=namespace
        )
        quite_count = getattr(args, 'quite', 0)
        verbose_count = getattr(args, 'verbose', 0)
        args.verbosity = verbose_count - quite_count
        return (args, argv)


class ParserBuilder(object):

    def __init__(self, prog, homepage, bugs_url, *args, **kwargs):
        self.prog = prog
        kwargs.setdefault(
            'epilog',
            os.linesep.join([
                'Report {prog} bugs to <{bugs_url}>',
                '{prog} home page: <{homepage}>'
            ]).format(prog=prog, homepage=homepage, bugs_url=bugs_url)
        )
        kwargs.setdefault('formatter_class', RawDescriptionHelpFormatter)
        self.parser = FinddArgumentParser(*args, prog=prog, **kwargs)
        self.subparsers = self.parser.add_subparsers()

    def add_version_argument(self, version):
        self.parser.add_argument(
            '--version',
            action='version',
            version=version
        )

    def add_init_parser(self):
        parser = self._add_subparser(
            'init',
            help='create a new Findd project',
        )
        parser.set_defaults(func=commands.init)

    def add_update_parser(self):
        parser = self._add_subparser(
            'update',
            help='update the index',
        )
        parser.set_defaults(func=commands.update)
        ParserBuilder._add_lazy_argument(parser)

    def add_list_parser(self):
        parser = self._add_subparser(
            'list',
            help='list duplicates tracked by the index',
        )
        parser.set_defaults(func=commands.list_duplicates)
        ParserBuilder._add_limit_argument(parser)
        ParserBuilder._add_skip_argument(parser)

    def add_run_parser(self):
        parser = self._add_subparser(
            'run',
            help='run a command for duplicates tracked by the index',
            epilog=os.linesep.join([
                'examples:',
                '  {prog} run -- mplayer',
                '  {prog} run --limit=1 -- ls -lh',
            ]).format(prog=self.prog),
            formatter_class=RawDescriptionHelpFormatter,
        )
        parser.set_defaults(func=commands.process_duplicates)
        parser.add_argument(
            'cmd',
            help='command to run for each set of duplicates',
        )
        parser.add_argument(
            'args',
            nargs='*',
            help='additional command args',
        )
        ParserBuilder._add_limit_argument(parser)
        ParserBuilder._add_skip_argument(parser)

    def _add_subparser(self, *args, **kwargs):
        subparser = self.subparsers.add_parser(*args, **kwargs)
        ParserBuilder._add_verbose_argument(subparser)
        return subparser

    def build(self):
        return self.parser

    @staticmethod
    def _add_verbose_argument(parser):
        parser.add_argument(
            '-v',
            '--verbose',
            default=0,
            action='count',
            help='be more verbose',
        )
        parser.add_argument(
            '-q',
            '--quite',
            default=0,
            action='count',
            help='be less verbose',
        )

    @staticmethod
    def _add_lazy_argument(parser):
        parser.add_argument(
            '-l',
            '--lazy',
            action='store_const',
            default=False,
            const=True,
            help='update hashes lazily',
        )

    @staticmethod
    def _add_skip_argument(parser):
        parser.add_argument(
            '-s',
            '--skip',
            metavar='N',
            nargs='?',
            default=0,
            type=int,
            help='skip N files per duplicate result set',
        )

    @staticmethod
    def _add_limit_argument(parser):
        parser.add_argument(
            '-l',
            '--limit',
            metavar='N',
            nargs='?',
            default=-1,
            type=int,
            help='limit duplicate result sets',
        )
