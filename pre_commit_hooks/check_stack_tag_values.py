from __future__ import annotations

import argparse
from typing import Sequence

from pre_commit_hooks import util


def get_valid_tag_values(files):
    valid_values = []
    for file in files:
        if file.startswith('https') or file.startswith('http'):
            content = util.get_url_content(file)
        else:
            content = util.get_local_content(file)

        valid_values.extend(content)
    return valid_values


def lint(files: list[str], tag: str, tag_value_files: [str]) -> bool:

    result = False
    valid_tag_values = get_valid_tag_values(tag_value_files)

    for file in files:
        config = util.load_config(file)
        if util.SCEPTRE_STACK_TAGS_KEY in config:
            stack_tags = config[util.SCEPTRE_STACK_TAGS_KEY]
            if tag not in stack_tags.keys():
                print(f'- {tag} not set in config file {file}')
                result = True
            else:
                tag_value = stack_tags[tag]
                if tag_value not in valid_tag_values:
                    print(f'- {tag_value} is not in valid set: {valid_tag_values}')
                    result = True
        else:
            print(f'- missing {util.SCEPTRE_STACK_TAGS_KEY} in config file {file}')
            result = True

    return result


def main(argv: Sequence[str] | None = None) -> int:
    """
    Check that the tags in the config file contain valid values
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '-t', '--tag',
        help='tag to validate',
    )
    parser.add_argument(
        '-f', '--file', action='append', default=[],
        help='file containing a list of valid tag values, '
             'may be specified multiple times',
    )
    args = parser.parse_args(argv)
    tag = args.tag
    tag_value_filess = args.file
    return int(lint(args.filenames, tag, tag_value_filess))


if __name__ == '__main__':
    raise SystemExit(main())