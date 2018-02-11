
import os
import re
import sys
import json
import codecs

from utils.output import *

def should_save_data(es_url_data, test_string, save_all=False):
    """Filter Data."""
    if save_all:
        return True

    if 'include' not in es_url_data and 'exclude' not in es_url_data:
        sys.stdout.write('+ ')
        return True

    if 'include' in es_url_data:
        combined_include = "(" + ")|(".join(es_url_data['include']) + ")"
        if re.match(combined_include, test_string):
            sys.stdout.write('+ ')
            return True

    if 'exclude' in es_url_data:
        combined_exclude = "(" + ")|(".join(es_url_data['exclude']) + ")"
        if re.match(combined_exclude, test_string):
            sys.stdout.write('- ')
            return False
    else:
        sys.stdout.write('- ')
        return False

    sys.stdout.write('+ ')
    return True


def save_objects(es_url_data, data, folder, save_all=False):
    """Save Objects."""
    print("Total '%s' objects found: %s" % (colorText(es_url_data['type'], WHITE),
                                            colorText(data['hits']['total'], WHITE)))

    for obj in data['hits']['hits']:
        if should_save_data(es_url_data, obj['_id'], save_all):
            print_color_text(obj['_id'], GREEN)

            ouput_file_path = os.path.join(folder, obj['_id']) + '.json'

            file = codecs.open(ouput_file_path, "w", "utf-8")
            file.write(json.dumps(obj['_source'], indent=4, sort_keys=False))
            file.close()
        else:
            print(obj['_id'])


def save_templates(es_url_data, data, folder, save_all=False):
    """Save Templates."""
    print("Total templates found: %d" % len(data))

    for template, template_data in data.iteritems():
        if should_save_data(es_url_data, template, save_all):
            print_color_text(template, GREEN)
            ouput_file_path = os.path.join(folder, template) + '.json'

            file = codecs.open(ouput_file_path, "w", "utf-8")
            file.write(json.dumps(template_data, indent=4, sort_keys=False))
            file.close()
        else:
            print(template)
