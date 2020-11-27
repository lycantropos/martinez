import pytest
from hypothesis import given

from tests.port_tests.hints import PortedSweepEvent
from . import strategies


@given(strategies.leaf_sweep_events)
def test_leaf(event: PortedSweepEvent) -> None:
    with pytest.raises(ValueError):
        event.is_vertical


@given(strategies.nested_sweep_events)
def test_nested(event: PortedSweepEvent) -> None:
    result = event.is_vertical

    assert isinstance(result, bool)
