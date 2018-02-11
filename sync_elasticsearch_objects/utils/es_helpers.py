

from elasticsearch import Elasticsearch, ConnectionError, TransportError


def get_all_indices(es, elasticsearch_host, index_names='*', index_status='open'):
    """Get All Indices."""
    indices = []
    arguments = {}

    arguments['index'] = index_names

    if index_status and 'none' not in index_status:
        arguments['expand_wildcards'] = index_status

    try:
        indices = es.indices.get_alias(**arguments).keys()
    except ConnectionError, e:
        print("ERROR: Hosts error: {0}".format(elasticsearch_host))
        print(e)
    except TransportError, e:
        print("ERROR: Index error: {0}".format(' '.join(index_names)))
        print(e)

    return indices
