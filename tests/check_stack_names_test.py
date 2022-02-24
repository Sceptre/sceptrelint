from __future__ import annotations

from pre_commit_hooks.check_stack_names import lint
from testing.util import get_resource_path

TEST_RESOURCES_DIR = 'check_stack_names'

def test_valid_stackname():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stackname_valid.yaml']
    assert lint(files) == False

def test_stackname_invalid_stack_name():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stackname_invalid.yaml']
    assert lint(files) == True

def test_stackname_invalid_stack_name_multiple_files():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [
        f'{resource_path}/stackname_valid.yaml',
        f'{resource_path}/stackname_invalid.yaml',
    ]
    assert lint(files) == True
