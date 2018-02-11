
import sys
import elasticsearch
import elasticsearch.helpers

from utils.output import *
from utils.es_helpers import get_all_indices


def reindex_via_api(es, index_names, reindex_suffix, reindex_force_delete, elasticsearch_host):
    """Reindex Elasticsearch"""
    header("Reindexing...\n{0}".format(elasticsearch_host))

    test_new_indices(es, index_names, reindex_suffix, reindex_force_delete, elasticsearch_host)

    indices = get_all_indices(es, elasticsearch_host, index_names)
    if not indices:
        return

    for index in indices:
        new_index_name = get_new_index_name(index, reindex_suffix)
        print_color_text("Creating index: {0}".format(new_index_name), GREEN)
        es.indices.create(new_index_name)

        print_color_text("Reindexing: {0} -> {1}".format(index, new_index_name), BLUE)
        elasticsearch.helpers.reindex(client=es, source_index=index, target_index=new_index_name)

        print_color_text("Closing index: {0}".format(index), YELLOW)
        es.indices.close(index=index)


def test_new_indices(es, index_names, reindex_suffix, reindex_force_delete, elasticsearch_host):
    """Test new indices."""
    indices = get_all_indices(es, elasticsearch_host, index_names)
    if not indices:
        return

    indices = sorted(indices)
    
    for index in indices:
        new_index_name = get_new_index_name(index, reindex_suffix)
        if new_index_name in indices:
            if reindex_force_delete:
                print_color_text("Deleting index: {0}".format(new_index_name), MAGENTA)
                es.indices.delete(new_index_name)
            else:
                print_color_text("ERROR: Target index already exists: {0}".format(new_index_name), RED)
                sys.exit(-1)


def get_new_index_name(index_name, reindex_suffix):
    """Get New Index Name."""
    new_index_name = index_name + reindex_suffix
    return new_index_name.lower()


def reindex_process():
    """Reindex Process."""
    pass
