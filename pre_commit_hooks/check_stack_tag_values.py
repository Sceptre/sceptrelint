from __future__ import annotations

import argparse
from typing import Sequence

from pre_commit_hooks import util


def get_valid_tag_values(
    files: list[str],
    tag_excludes: list[str]) -> list[str]:
    """
    Get a list of valid tag values from a list of file references. Exclude tags
    from the valid tag list if a list of exluded tags are provides.
    """

    tags_from_files = []
    for file in files:
        if file.startswith('https') or file.startswith('http'):
            content = util.get_url_content(file)
        else:
            content = util.get_local_content(file)

        tags_from_files.extend(content)

    valid_values = list(set(tags_from_files).difference(tag_excludes))
    return valid_values


def lint(
    files: list[str],
    tag: str, tag_value_files: list[str],
    tag_excludes: list[str]) -> bool:
    """
    Check that the tags in the config file contain valid values
    """

    result = False
    valid_tag_values = get_valid_tag_values(tag_value_files, tag_excludes)

    for file in files:
        config = util.load_config(file)
        if util.SCEPTRE_STACK_TAGS_KEY in config:
            stack_tags = config[util.SCEPTRE_STACK_TAGS_KEY]
            if tag not in stack_tags:
                print(f'- {file}: {tag} tag is not set')
                result = True
            else:
                tag_value = stack_tags[tag]
                if tag_value not in valid_tag_values:
                    print(f'- {file}: "{tag_value}" is not a valid {tag}')
                    result = True
        else:
            print(f'- {file}: {util.SCEPTRE_STACK_TAGS_KEY} parameter is not defined')
            result = True

    return result


def main(argv: Sequence[str] | None = None) -> int:
    """
    Execute the linter, either manually or by pre-commit
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
    parser.add_argument(
        '-e', '--exclude', action='append', default=[],
        help='tag to remove from the valid tag values list, '
             'may be specified multiple times',
    )
    args = parser.parse_args(argv)
    tag = args.tag
    tag_value_files = args.file
    tag_excludes = args.exclude
    return int(lint(args.filenames, tag, tag_value_files, tag_excludes))


if __name__ == '__main__':
    raise SystemExit(main())
