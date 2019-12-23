import copy

from hypothesis import given

from martinez.boolean import SweepEvent
from . import strategies


@given(strategies.sweep_events)
def test_shallow(sweep_event: SweepEvent) -> None:
    result = copy.copy(sweep_event)

    assert result is not sweep_event
    assert result == sweep_event


@given(strategies.sweep_events)
def test_deep(sweep_event: SweepEvent) -> None:
    result = copy.deepcopy(sweep_event)

    assert result is not sweep_event
    assert result == sweep_event
