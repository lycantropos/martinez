import pytest
from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from . import strategies


@given(strategies.leaf_sweep_events)
def test_leaf(event: BoundSweepEvent) -> None:
    with pytest.raises(ValueError):
        event.is_vertical


@given(strategies.nested_sweep_events)
def test_nested(event: BoundSweepEvent) -> None:
    result = event.is_vertical

    assert isinstance(result, bool)
