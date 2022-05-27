from __future__ import annotations

from pre_commit_hooks.check_stack_tag_values import lint
from testing.util import get_resource_path

TEST_RESOURCES_DIR = 'check_stack_tag_values'


def test_stack_tags_key_exist_value_valid_single_file():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_match_tag_values1.yaml']
    assert not lint(files, 'color', [f'{resource_path}/tag_values1.json'])


def test_stack_tags_key_exist_value_valid_multiple_files():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_match_tag_values2.yaml']
    assert not lint(
        files, 'color', [
            f'{resource_path}/tag_values1.json',
            f'{resource_path}/tag_values2.json',
        ],
    )


def test_stack_tags_key_missing():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_missing.yaml']
    assert lint(files, 'color', [f'{resource_path}/tag_values1.json'])


def test_stack_tags_tag_non_matching_value():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_non_matching_value.yaml']
    assert lint(files, 'color', [f'{resource_path}/tag_values1.json'])


def test_stack_tags_tag_missing():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_missing.yaml']
    assert lint(files, 'color', [f'{resource_path}/tag_values1.json'])


def test_stack_tags_tag_not_in_config_file():
    resource_path = get_resource_path(TEST_RESOURCES_DIR)
    files = [f'{resource_path}/stack_tags_tag_not_set.yaml']
    assert lint(files, 'color', [f'{resource_path}/tag_values1.json'])
