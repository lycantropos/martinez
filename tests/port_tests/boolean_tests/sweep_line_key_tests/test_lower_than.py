from typing import Any

import pytest
from hypothesis import given

from martinez.boolean import SweepLineKey
from tests.utils import (equivalence)
from . import strategies


@given(strategies.nested_sweep_line_keys)
def test_irreflexivity(sweep_line_key: SweepLineKey) -> None:
    assert not sweep_line_key < sweep_line_key


@given(strategies.nested_sweep_line_keys, strategies.nested_sweep_line_keys)
def test_connection_with_greater_than(first_key: SweepLineKey,
                                      second_key: SweepLineKey) -> None:
    assert equivalence(first_key < second_key, second_key > first_key)


@given(strategies.nested_sweep_line_keys, strategies.non_sweep_line_keys)
def test_non_key(key: SweepLineKey, non_key: Any) -> None:
    with pytest.raises(TypeError):
        key < non_key
