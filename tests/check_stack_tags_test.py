from __future__ import annotations

from pre_commit_hooks.check_stack_tags import lint
from testing.util import get_resource_path

TEST_RESOURCES_DIR = 'check_stack_tags'


def test_stack_tags_key_exists():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_one_tag.yaml']
    assert not lint(files, [])


def test_stack_tags_key_missing():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_missing.yaml']
    assert lint(files, [])


def test_stack_one_tag_exist():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_one_tag.yaml']
    assert not lint(files, ['foo'])


def test_stack_multiple_tag_exists():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_multiple_tags.yaml']
    assert not lint(files, ['one', 'two'])


def test_stack_tags_tag_missing():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_multiple_tags.yaml']
    assert lint(files, ['three'])
