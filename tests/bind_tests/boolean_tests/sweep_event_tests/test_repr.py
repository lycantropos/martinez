import sys

from _martinez import SweepEvent
from hypothesis import given

from . import strategies


@given(strategies.sweep_events)
def test_basic(sweep_event: SweepEvent) -> None:
    result = repr(sweep_event)

    assert result.startswith(SweepEvent.__module__)
    assert SweepEvent.__qualname__ in result


@given(strategies.acyclic_sweep_events)
def test_round_trip(sweep_event: SweepEvent) -> None:
    result = repr(sweep_event)

    assert eval(result, sys.modules) == sweep_event
