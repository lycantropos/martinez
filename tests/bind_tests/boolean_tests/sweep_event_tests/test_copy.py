import copy

from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from . import strategies


@given(strategies.sweep_events)
def test_shallow(event: BoundSweepEvent) -> None:
    result = copy.copy(event)

    assert result is not event
    assert result == event


@given(strategies.sweep_events)
def test_deep(event: BoundSweepEvent) -> None:
    result = copy.deepcopy(event)

    assert result is not event
    assert result == event
