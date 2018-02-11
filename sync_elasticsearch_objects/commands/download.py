
import os
import re

from utils.output import *
from es_api import elasticsearch_api_request
from es_api.save import *


def download_via_api(sync_object,
                     es_url_data,
                     elasticsearch_host,
                     max_size,
                     folder,
                     save_all=False,
                     debug=False,
                     dry_run=False):
    """Download from Elasticsearch."""
    header("Downloading ({0})...\n{1}".format(sync_object, elasticsearch_host))
    sub_header(folder)

    if not os.path.isdir(folder):
        os.makedirs(folder)

    es_url = '/'.join([elasticsearch_host,
                      es_url_data['index'],
                      es_url_data['type']])
    es_url = es_url.rstrip('/')

    es_command = False
    if re.match('^_', es_url_data['index']):
        url = es_url
        es_command = True
    else:
        url = "%s/_search" % (es_url)

    # url += '?pretty=true' # NOTE: pretty output is done by 'json.dumps' in function 'save_objects'
    url += "?size=%s" % max_size

    data = elasticsearch_api_request(url, 'GET', debug=debug, dry_run=dry_run)

    if dry_run:
        return

    if es_command:
        save_templates(es_url_data, data, folder, save_all)
    else:
        save_objects(es_url_data, data, folder, save_all)
