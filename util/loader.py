import os
import yaml


def default_yaml_path():
    this_file_path = os.path.abspath(__file__)
    root_dir_path = os.path.dirname(os.path.dirname(this_file_path))
    return os.path.join(root_dir_path, 'config.yaml')


def load_yaml(path: str = None):
    global config
    if config is None:
        if path is None:
            path = default_yaml_path()
        with open(path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
