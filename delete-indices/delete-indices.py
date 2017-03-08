#!/usr/bin/env python

# NOTE: Why delete_by_query can also be used the following script will allow a dry run.

import argparse
import re

from elasticsearch import Elasticsearch, ConnectionError, TransportError


def _parse_args():
    """Parse Command Arguments."""
    desc = 'Delete elasticsearch indices'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('hosts',
                        nargs='+',
                        help='Elasticsearch Hosts')
    parser.add_argument('-s', '--status',
                        nargs='+',
                        default=['closed'],
                        choices=['all', 'open', 'closed', 'none'],
                        help='Elasticsearch indices status')
    parser.add_argument('-n', '--index-names',
                        nargs='+',
                        default=[],
                        help='Specific index names')
    parser.add_argument('-i', '--index',
                        default='',
                        help='RegEx index name')
    parser.add_argument('-e', '--exclude-indexes',
                        nargs='+',
                        default=['.kibana'],
                        help='Exclude indexes')
    parser.add_argument('--dry-run',
                        action='store_true',
                        default=False,
                        help='Dry-run. No action taken')

    return parser.parse_args()


def main():
    """Main."""
    args = _parse_args()

    if args.dry_run:
        print("WARN: Executing in Dry-Run mode. No action will be taken!")

    if args.index_names:
        print("WARN: Deleting specific indexes: {0}".format(' '.join(args.index_names)))

    print("INFO: Deleting indices with status: {0}".format(' '.join(args.status)))

    es = Elasticsearch(args.hosts)
    print("INFO: Cluster Health: {0}".format(es.cluster.health()['status']))

    if 'none' in args.status:
        print("INFO: Status 'none' specified. Therefore all indices will be deleted!")

    indices = []
    arguments = {}
    if args.index_names:
        remove_index_from_list = []
        for index_name in args.index_names:
            if not es.indices.exists(index=index_name):
                print("WARN: Index not found. Removing it from list: {0}".format(index_name))
                remove_index_from_list.append(index_name)

        for remove_index in remove_index_from_list:
            args.index_names.remove(remove_index)

        if not args.index_names:
            return

        arguments['index'] = args.index_names

    if args.status and 'none' not in args.status:
        arguments['expand_wildcards'] = args.status

    try:
        indices = es.indices.get_alias(**arguments).keys()
    except ConnectionError, e:
        print("ERROR: Hosts error: {0}".format(args.hosts))
        print(e)
    except TransportError, e:
        print("ERROR: Index error: {0}".format(args.index_names))
        print(e)

    if not indices:
        return

    sorted(indices)

    for exclude_index in args.exclude_indexes:
        if exclude_index in indices:
            print("INFO: Index '{0}' is excluded and will not be deleted!".format(exclude_index))
            indices.remove(exclude_index)

    for index in indices:
        if args.index:
            if not re.search(args.index, index):
                continue

        print(index)

        if not args.dry_run:
            es.indices.delete(index)

if __name__ == "__main__":
    main()
