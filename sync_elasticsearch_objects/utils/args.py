
import os
import sys
import argparse

from argparse import ArgumentDefaultsHelpFormatter,RawDescriptionHelpFormatter
from utils.output import *


# https://stackoverflow.com/questions/34544752/argparse-and-argumentdefaultshelpformatter-formatting-of-default-values-when-sy
class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    if type(action.default) == type(sys.stdin):
                        print(action.default.name)
                        help += ' (default: ' + str(action.default.name) + ')'
                    else:
                        help += ' (default: %(default)s)'
        return help


def parse_args():
    """Parse Args."""
    args_epilog = """
e.g.

  {0} http://elk-server:9200 <TASK>

    """.format(os.path.basename(__file__))

    parser = argparse.ArgumentParser(description='Syncs Elasticsearch and Kibana Objects',
                                     formatter_class=CustomFormatter,
                                     epilog=args_epilog)
    parser.add_argument('elasticsearch_host',
                        nargs='?',
                        default='http://10.10.10.10:9200',
                        help='Elasticsearch Host')

    task_args_group = parser.add_argument_group('TASKS')
    task_args_group.add_argument('--download',
                        action='store_true',
                        default=False,
                        help='Download objects and templates from Elasticsearch')

    task_args_group.add_argument('--upload',
                        action='store_true',
                        default=False,
                        help='Upload objects and templates to Elasticsearch')

    task_args_group.add_argument('--reindex',
                        nargs='+',
                        default=[],
                        help='Reindex Elasticsearch indices')

    task_args_group.add_argument('--delete',
                        action='store_true',
                        default=False,
                        help='Delete objects and templates from Elasticsearch')

    download_args_group = parser.add_argument_group('Download Options')
    download_args_group.add_argument('--save-all',
                        action='store_true',
                        default=False,
                        help='Saves All Data')
    download_args_group.add_argument('--max_size',
                        type=int,
                        default='1024',
                        help='Elasticsearch Download Max Hit Size')

    reindex_args_group = parser.add_argument_group('Reindex Options')
    reindex_args_group.add_argument('--reindex_suffix',
                        type=str,
                        default='_v1',
                        help='Suffix for the new target index')
    reindex_args_group.add_argument('--reindex_force_delete',
                        action='store_true',
                        default=False,
                        help='Delete new target index if it exists')

    options_args_group = parser.add_argument_group('General Options')
    options_args_group.add_argument('--config',
                        type=str,
                        default='sync_elasticsearch_objects.yml',
                        help='Config File')
    options_args_group.add_argument('--sync_local_folder',
                        type=str,
                        default='_OUTPUT',
                        help='Sync local Folder')
    options_args_group.add_argument('--debug',
                        action='store_true',
                        default=False,
                        help='Debug output')
    options_args_group.add_argument('--dry-run',
                        action='store_true',
                        default=False,
                        help='Dry-run. No action taken')

    args = parser.parse_args()

    if not args.download \
       and not args.upload \
       and not args.reindex \
       and not args.delete \
       and not args.save_all:
        parser.print_help()
        sys.exit(-1)

    args.elasticsearch_host = args.elasticsearch_host.rstrip('/')

    if args.dry_run:
        print_color_text("WARN: Executing in Dry-Run mode. No action will be taken!", RED)

    return args
