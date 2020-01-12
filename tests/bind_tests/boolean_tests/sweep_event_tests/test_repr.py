import sys

from _martinez import SweepEvent
from hypothesis import given

from . import strategies


@given(strategies.sweep_events)
def test_basic(event: SweepEvent) -> None:
    result = repr(event)

    assert result.startswith(SweepEvent.__module__)
    assert SweepEvent.__qualname__ in result


@given(strategies.acyclic_sweep_events)
def test_round_trip(event: SweepEvent) -> None:
    result = repr(event)

    assert eval(result, sys.modules) == event
