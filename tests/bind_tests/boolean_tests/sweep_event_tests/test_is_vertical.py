import pytest
from _martinez import SweepEvent
from hypothesis import given

from . import strategies


@given(strategies.leaf_sweep_events)
def test_leaf(event: SweepEvent) -> None:
    with pytest.raises(ValueError):
        event.is_vertical


@given(strategies.nested_sweep_events)
def test_nested(event: SweepEvent) -> None:
    result = event.is_vertical

    assert isinstance(result, bool)
