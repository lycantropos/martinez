import sys

from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from . import strategies


@given(strategies.sweep_events)
def test_basic(event: BoundSweepEvent) -> None:
    result = repr(event)

    assert result.startswith(BoundSweepEvent.__module__)
    assert BoundSweepEvent.__qualname__ in result


@given(strategies.acyclic_sweep_events)
def test_round_trip(event: BoundSweepEvent) -> None:
    result = repr(event)

    assert eval(result, sys.modules) == event
