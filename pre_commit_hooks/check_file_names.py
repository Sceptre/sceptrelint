from __future__ import annotations

import argparse
import os
from typing import Sequence

from pre_commit_hooks import util

def lint(files: list[str]) -> bool:

    result = False
    for file in files:
        config = util.load_config(file)
        stack_name = config['stack_name']
        path, file_extension = os.path.splitext(file)
        filename = path.split('/')[-1] + '.yaml'
        if (stack_name + file_extension) != filename:
            print(f'- stack name does not match file name [{file}]')
            result = True

    return result

def main(argv: Sequence[str] | None = None) -> int:
    """
    Check that the `stack_name` matches the file name
    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-parameters.html
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return int(lint(args.filenames))


if __name__ == '__main__':
    raise SystemExit(main())
