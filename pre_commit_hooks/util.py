from __future__ import annotations

import json
import os
import re
from urllib.parse import urlparse

import requests
import yaml
from jinja2 import Template

SCEPTRE_STACK_TAGS_KEY = 'stack_tags'
SCEPTRE_STACK_NAME_KEY = 'stack_name'
STACK_NAME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-]{0,127}$')


def load_config(config_path: str) -> dict[str, str]:
    """
    Produce a Python object (usually dict-like) from the config file
    at `config_path`

    :param config_path: path to config file, can be absolute or relative to
                        working directory
    :return: Python object representing structure of config file
    """

    # Let YAML handle tags naively
    def default_constructor(loader, tag_suffix, node):
        return tag_suffix + ' ' + node.value
    yaml.FullLoader.add_multi_constructor('', default_constructor)

    with open(config_path) as new_file:
        # Load template with blanks for all variables
        template = Template(new_file.read())
        return yaml.load(template.render(stack_group_config=''), Loader=yaml.FullLoader)


def get_local_content(path):
    """
    Gets file contents from a file on the local machine
    :param path: The absolute path to a file
    """
    try:
        filename, file_extension = os.path.splitext(path)
        with open(path) as file:
            content = file.read()
    except (OSError, TypeError) as e:
        raise e

    if content:
        if file_extension == '.json':
            content = json.loads(content)
        if file_extension == '.yaml' or file_extension == '.yml':
            content = yaml.safe_load(content)

    return content


def get_url_content(path):
    """
    Gets file contents from a file at a URL location
    :param path: The URL reference to a file
    """
    url = urlparse(path)
    filename, file_extension = os.path.splitext(url.path)
    try:
        response = requests.get(path)
        content = response.text
        if response.status_code != requests.codes.ok:
            raise response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e

    if content:
        if file_extension == '.json':
            content = json.loads(content)
        if file_extension == '.yaml' or file_extension == '.yml':
            content = yaml.safe_load(content)

    return content
