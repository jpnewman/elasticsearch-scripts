#!/usr/bin/env python

"""This script syncs Elasticsearch and Kibana objects."""

import fnmatch
import codecs
import json
import sys
import os
import re

from utils.args import *
from utils.config import *
from utils.output import *

from commands.download import download_via_api
from commands.reindex import reindex_via_api
from commands.upload import upload_via_api
from commands.delete import delete_via_api

from elasticsearch import Elasticsearch


# Main
def main():
    """Main."""
    args = parse_args()
    config = load_config(args.config)

    es = Elasticsearch(args.elasticsearch_host)

    for sync_object, es_url_data in config['sync_objects'].iteritems():
        folder = os.path.join(args.sync_local_folder, sync_object)

        if args.download:
            download_via_api(sync_object,
                             es_url_data,
                             args.elasticsearch_host,
                             args.max_size,
                             folder,
                             args.save_all,
                             args.debug,
                             args.dry_run)

        elif args.reindex:
            if sync_object == 'mapping':
                reindex_via_api(es,
                                args.reindex,
                                args.reindex_suffix,
                                args.reindex_force_delete,
                                args.elasticsearch_host)

        elif args.upload:
            if sync_object != 'mapping':
                upload_via_api(sync_object,
                               es_url_data,
                               args.elasticsearch_host,
                               folder,
                               args.debug,
                               args.dry_run)

        elif args.delete:
            delete_via_api(sync_object,
                           es_url_data,
                           args.elasticsearch_host,
                           folder,
                           args.debug,
                           args.dry_run)


if __name__ == "__main__":
    main()
