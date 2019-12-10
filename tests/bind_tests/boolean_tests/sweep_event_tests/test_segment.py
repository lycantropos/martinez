import pytest
from _martinez import (Segment,
                       SweepEvent)
from hypothesis import given

from . import strategies


@given(strategies.leaf_sweep_events)
def test_leaf(sweep_event: SweepEvent) -> None:
    with pytest.raises(ValueError):
        sweep_event.segment


@given(strategies.nested_sweep_events)
def test_nested(sweep_event: SweepEvent) -> None:
    result = sweep_event.segment

    assert isinstance(result, Segment)
