from __future__ import annotations

import argparse
from typing import Sequence

from pre_commit_hooks import util


def lint(files: list[str], tags: list[str]) -> bool:

    result = False
    for file in files:
        config = util.load_config(file)
        if util.SCEPTRE_STACK_TAGS_KEY in config:
            if config[util.SCEPTRE_STACK_TAGS_KEY]:
                for tag in tags:
                    if tag not in config[util.SCEPTRE_STACK_TAGS_KEY]:
                        print(f'- {util.SCEPTRE_STACK_TAGS_KEY} is missing {tag} [{file}]')
                        result = True
            else:
                print(f'- missing {util.SCEPTRE_STACK_TAGS_KEY} [{file}]')
                result = True
        else:
            print(f'- missing {util.SCEPTRE_STACK_TAGS_KEY} definition [{file}]')
            result = True

    return result


def main(argv: Sequence[str] | None = None) -> int:
    """
    Check that the config file contains specific tags
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '-t', '--tag', action='append', default=[],
        help='tag to check, may be specified multiple times',
    )
    args = parser.parse_args(argv)

    return int(lint(args.filenames, args.tag))


if __name__ == '__main__':
    raise SystemExit(main())
