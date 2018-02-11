
import os

from utils.output import *
from utils.files import get_local_files
from es_api import elasticsearch_api_request


def delete_via_api(sync_object, es_url_data, elasticsearch_host, folder, debug=False, dry_run=False):
    """Delete found local objects from Elasticsearch."""
    header("Deleting ({0})...\n{1}".format(sync_object, elasticsearch_host))
    sub_header(folder)

    files = get_local_files(folder)

    for filename in files:
        file_title = os.path.basename(os.path.splitext(filename)[0])
        print(file_title)

        es_url = '/'.join([elasticsearch_host,
                          es_url_data['index'],
                          es_url_data['type']])
        es_url = es_url.rstrip('/')

        url = "%s/%s" % (es_url,
                         file_title)

        elasticsearch_api_request(url, 'DELETE', debug=debug, dry_run=dry_run)
