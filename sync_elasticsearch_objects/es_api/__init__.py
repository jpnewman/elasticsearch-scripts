
import json
import urllib2

from utils.output import *


def elasticsearch_api_request(url, method='GET', filename=None, debug=False, dry_run=False):
    """Elasticsearch API request."""
    data = {}

    curl_url = "curl -X%s %s" % (method, url)

    if filename:
        curl_url = "curl -X%s %s -T %s" % (method, url, filename)

    if debug:
        print_color_text(curl_url, MAGENTA)
    elif filename:
        print_color_text(filename, MAGENTA)

    opener = urllib2.build_opener(urllib2.HTTPHandler)

    if filename:
        with open(filename) as f:
            file_data = f.read()

        request = urllib2.Request(url,
                                  data=file_data)

        request.add_header('Content-Type', 'application/json')
    else:
        request = urllib2.Request(url)

    request.get_method = lambda: method

    if dry_run:
        return data

    try:
        response = opener.open(request)

        data = json.loads(response.read())

        report_api_response(data)

    except urllib2.HTTPError as err:
        if err.code == 400:
            if not debug:
                print_color_text("ERROR: %s" % curl_url, RED)
            raise
        if err.code == 404:
            print("WARN: File not found: %s" % url)
        else:
            raise

    return data


def report_api_response(json_data):
    """Report API response."""
    output_data_name_dict = {
        "_version": "Version",
        "created": "Created",
        "acknowledged": "Acknowledged"
    }

    response_arr = []
    for json_name, name in output_data_name_dict.iteritems():
        if json_name in json_data:
            response_arr.append("%s: %r" % (name,
                                            json_data[json_name]))

    print('\t'.join(response_arr))

    if '_shards' in json_data and json_data['_shards']['failed']:
        print("ERROR: Upload failed!")
