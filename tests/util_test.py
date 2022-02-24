from __future__ import annotations

from pre_commit_hooks.util import load_config
from testing.util import TESTING_DIR


def test_load_config():
    expected = {
        'template': {
            'path': 'template.yaml',
        }, 'stack_name': 'simple-config',
    }
    config = load_config(f'{TESTING_DIR}/resources/sceptre_config.yaml')
    assert config == expected
