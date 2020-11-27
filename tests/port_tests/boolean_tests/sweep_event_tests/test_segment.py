import pytest
from hypothesis import given

from tests.port_tests.hints import (PortedSegment,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.leaf_sweep_events)
def test_leaf(event: PortedSweepEvent) -> None:
    with pytest.raises(ValueError):
        event.segment


@given(strategies.nested_sweep_events)
def test_nested(event: PortedSweepEvent) -> None:
    result = event.segment

    assert isinstance(result, PortedSegment)
