from __future__ import annotations

from pre_commit_hooks.check_file_names import lint
from testing.util import get_resource_path

TEST_RESOURCES_DIR = 'check_file_names'


def test_stackname_matches_filename():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stackname_matches_filename.yaml']
    assert not lint(files)


def test_stackname_not_match_filename():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stackname_not_match_filename.yaml']
    assert lint(files)


def test_stackname_not_match_filename_multiple_files():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [
        f'{resource_path}/stackname_matches_filename.yaml',
        f'{resource_path}/stackname_not_match_filename.yaml',
    ]
    assert lint(files)
