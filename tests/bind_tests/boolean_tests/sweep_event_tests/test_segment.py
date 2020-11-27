import pytest
from hypothesis import given

from tests.bind_tests.hints import (BoundSweepEvent, BoundSegment)
from . import strategies


@given(strategies.leaf_sweep_events)
def test_leaf(event: BoundSweepEvent) -> None:
    with pytest.raises(ValueError):
        event.segment


@given(strategies.nested_sweep_events)
def test_nested(event: BoundSweepEvent) -> None:
    result = event.segment

    assert isinstance(result, BoundSegment)
