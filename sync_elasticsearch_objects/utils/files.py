
import os
import fnmatch


def get_local_files(folder, file_filter='*.json'):
    """Get local Objects."""
    found_files = []
    for root, dirs, files in os.walk(folder):
        for filename in fnmatch.filter(files, file_filter):
            found_files.append(os.path.join(root, filename))

    return found_files
