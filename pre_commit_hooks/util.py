from __future__ import annotations

import re

from jinja2 import Template
from yaml import FullLoader
from yaml import load

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
    FullLoader.add_multi_constructor('', default_constructor)

    with open(config_path) as new_file:
        # Load template with blanks for all variables
        template = Template(new_file.read())
        return load(template.render(stack_group_config=''), Loader=FullLoader)
