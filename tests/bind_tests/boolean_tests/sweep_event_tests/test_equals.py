from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.sweep_events)
def test_reflexivity(event: BoundSweepEvent) -> None:
    assert event == event


@given(strategies.sweep_events, strategies.sweep_events)
def test_symmetry(first_event: BoundSweepEvent,
                  second_event: BoundSweepEvent) -> None:
    assert equivalence(first_event == second_event,
                       second_event == first_event)


@given(strategies.sweep_events, strategies.sweep_events,
       strategies.sweep_events)
def test_transitivity(first_event: BoundSweepEvent,
                      second_event: BoundSweepEvent,
                      third_event: BoundSweepEvent) -> None:
    assert implication(first_event == second_event
                       and second_event == third_event,
                       first_event == third_event)


@given(strategies.sweep_events, strategies.sweep_events)
def test_connection_with_inequality(first_event: BoundSweepEvent,
                                    second_event: BoundSweepEvent) -> None:
    assert equivalence(not first_event == second_event,
                       first_event != second_event)
