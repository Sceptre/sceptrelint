from __future__ import annotations

import json
import os
import re
from typing import Any
from urllib.parse import urlparse

import requests
import yaml
from jinja2 import Template

SCEPTRE_STACK_TAGS_KEY = 'stack_tags'
SCEPTRE_STACK_NAME_KEY = 'stack_name'
STACK_NAME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-]{0,127}$')


def load_config(config_path: str) -> Any:
    """
    Produce a Python object (usually dict-like) from the config file
    at `config_path`

    :param config_path: path to config file, can be absolute or relative to
                        working directory
    :return: Python object representing structure of config file
    """

    # Let YAML handle tags naively
    def default_constructor(loader: Any, tag_suffix: Any, node: Any) -> str:
        return tag_suffix + ' ' + node.value
    yaml.FullLoader.add_multi_constructor('', default_constructor)

    with open(config_path, encoding='utf-8') as new_file:
        # Load template with blanks for all variables
        template = Template(new_file.read())
        return yaml.load(template.render(stack_group_config=''), Loader=yaml.FullLoader)


def get_local_content(path: str) -> list[str]:
    """
    Gets file contents from a file on the local machine
    :param path: The absolute path to a file
    The path can reference a file containing yaml or json content.
    The default is to assume json content.
    """
    try:
        filename, file_extension = os.path.splitext(path)
        with open(path, encoding='utf-8') as file:
            raw_content = file.read()
    except (OSError, TypeError) as e:
        raise e

    content = []
    if raw_content:
        if file_extension == '.yaml' or file_extension == '.yml':
            content = yaml.safe_load(raw_content)
        else:
            content = json.loads(raw_content)

    return content


def get_url_content(path: str) -> list[str]:
    """
    Gets file contents from a file at a URL location
    :param path: The URL reference to a file
    The path can reference a file containing yaml or json content.
    The default is to assume json content.
    """
    url = urlparse(path)
    filename, file_extension = os.path.splitext(url.path)
    try:
        response = requests.get(path)
        raw_content = response.text
        if response.status_code != requests.codes.ok:
            raise requests.exceptions.HTTPError(raw_content)
    except requests.exceptions.RequestException as e:
        raise e

    content = []
    if raw_content:
        if file_extension == '.yaml' or file_extension == '.yml':
            content = yaml.safe_load(raw_content)
        else:
            content = json.loads(raw_content)

    return content


def get_content(file: str) -> list[str]:

    if file.startswith('http'):
        content = get_url_content(file)
    else:
        content = get_local_content(file)

    return content
