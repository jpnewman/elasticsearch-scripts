#!/usr/bin/env python

import argparse

from elasticsearch import Elasticsearch, ConnectionError


def _parse_args():
    """Parse Command Arguments."""
    desc = 'Delete elasticsearch indices'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('hosts',
                        nargs='+',
                        help='Elasticsearch Hosts')
    parser.add_argument('-s', '--status',
                        nargs=1,
                        type=str,
                        default=['closed'],
                        choices=['all', 'open', 'closed', 'none'],
                        help='Elasticsearch indices status')
    parser.add_argument('--dry-run',
                        action='store_true',
                        default=False,
                        help='Dry-run. No action taken')

    args = parser.parse_args()
    args.status = str(args.status[0]).lower()

    return args


def main():
    """Main."""
    args = _parse_args()

    if args.dry_run:
        print("WARN: Executing in Dry-Run mode. No action will be taken!")

    print("INFO: Deleting indices with status: {0}".format(args.status))

    es = Elasticsearch(args.hosts)

    try:
        if args.status == 'none':
            indices = es.indices.get_alias().keys()
        else:
            indices = es.indices.get_alias(expand_wildcards=args.status).keys()
    except ConnectionError:
        print("ERROR: Hosts not found: {0}".format(args.hosts))
        raise

    sorted(indices)

    for index in indices:
        print(index)

        if not args.dry_run:
            es.indices.delete(index)

if __name__ == "__main__":
    main()
