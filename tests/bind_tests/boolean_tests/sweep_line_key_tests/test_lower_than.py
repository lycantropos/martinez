from typing import Any

import pytest
from hypothesis import given

from tests.bind_tests.hints import BoundSweepLineKey
from tests.utils import equivalence
from . import strategies


@given(strategies.nested_sweep_line_keys)
def test_irreflexivity(key: BoundSweepLineKey) -> None:
    assert not key < key


@given(strategies.nested_sweep_line_keys,
       strategies.nested_sweep_line_keys)
def test_connection_with_greater_than(first_key: BoundSweepLineKey,
                                      second_key: BoundSweepLineKey) -> None:
    assert equivalence(first_key < second_key, second_key > first_key)


@given(strategies.nested_sweep_line_keys, strategies.non_sweep_line_keys)
def test_non_key(key: BoundSweepLineKey, non_key: Any) -> None:
    with pytest.raises(TypeError):
        key < non_key
