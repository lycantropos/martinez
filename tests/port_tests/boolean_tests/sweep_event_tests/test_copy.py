import copy

from hypothesis import given

from martinez.boolean import SweepEvent
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
