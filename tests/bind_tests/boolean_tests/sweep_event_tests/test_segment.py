import pytest
from _martinez import (Segment,
                       SweepEvent)
from hypothesis import given

from . import strategies


@given(strategies.leaf_sweep_events)
def test_leaf(event: SweepEvent) -> None:
    with pytest.raises(ValueError):
        event.segment


@given(strategies.nested_sweep_events)
def test_nested(event: SweepEvent) -> None:
    result = event.segment

    assert isinstance(result, Segment)
