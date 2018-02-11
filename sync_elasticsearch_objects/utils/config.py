
import yaml


def load_config(config_file):
    """Load Config."""
    config = {}

    with open(config_file) as f:
        config = yaml.load(f)

    return config
