from typing import (Any,
                    Tuple)

import pytest
from hypothesis import given

from martinez.boolean import SweepLineKey
from tests.utils import equivalence
from . import strategies


@given(strategies.nested_sweep_line_keys)
def test_irreflexivity(key: SweepLineKey) -> None:
    assert not key < key


@given(strategies.nested_sweep_line_keys_pairs)
def test_connection_with_greater_than(keys_pair: Tuple[SweepLineKey,
                                                       SweepLineKey]) -> None:
    first_key, second_key = keys_pair

    assert equivalence(first_key < second_key, second_key > first_key)


@given(strategies.nested_sweep_line_keys, strategies.non_sweep_line_keys)
def test_non_key(key: SweepLineKey, non_key: Any) -> None:
    with pytest.raises(TypeError):
        key < non_key
