import copy

from hypothesis import given

from tests.port_tests.hints import PortedSweepEvent
from . import strategies


@given(strategies.sweep_events)
def test_shallow(event: PortedSweepEvent) -> None:
    result = copy.copy(event)

    assert result is not event
    assert result == event


@given(strategies.sweep_events)
def test_deep(event: PortedSweepEvent) -> None:
    result = copy.deepcopy(event)

    assert result is not event
    assert result == event
