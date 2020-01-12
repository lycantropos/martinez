import copy

from _martinez import SweepEvent
from hypothesis import given

from . import strategies


@given(strategies.sweep_events)
def test_shallow(event: SweepEvent) -> None:
    result = copy.copy(event)

    assert result is not event
    assert result == event


@given(strategies.sweep_events)
def test_deep(event: SweepEvent) -> None:
    result = copy.deepcopy(event)

    assert result is not event
    assert result == event
