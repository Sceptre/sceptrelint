from __future__ import annotations

import argparse
import re
from typing import Sequence

from pre_commit_hooks import util


def lint(files: list[str]) -> bool:

    result = False
    for file in files:
        config = util.load_config(file)
        stack_name = config[util.SCEPTRE_STACK_NAME_KEY]
        if not re.match(util.STACK_NAME_PATTERN, stack_name):
            print(f'- {stack_name} is an invalid stack name [{file}]')
            result = True

    return result


def main(argv: Sequence[str] | None = None) -> int:
    """
    Check that the `stack_name` value conforms to AWS cloudformation requirements
    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-parameters.html
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return int(lint(args.filenames))


if __name__ == '__main__':
    raise SystemExit(main())
