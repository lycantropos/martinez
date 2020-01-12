from _martinez import SweepEvent
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.sweep_events)
def test_reflexivity(event: SweepEvent) -> None:
    assert event == event


@given(strategies.sweep_events, strategies.sweep_events)
def test_symmetry(first_event: SweepEvent,
                  second_event: SweepEvent) -> None:
    assert equivalence(first_event == second_event,
                       second_event == first_event)


@given(strategies.sweep_events, strategies.sweep_events,
       strategies.sweep_events)
def test_transitivity(first_event: SweepEvent,
                      second_event: SweepEvent,
                      third_event: SweepEvent) -> None:
    assert implication(first_event == second_event
                       and second_event == third_event,
                       first_event == third_event)


@given(strategies.sweep_events, strategies.sweep_events)
def test_connection_with_inequality(first_event: SweepEvent,
                                    second_event: SweepEvent) -> None:
    assert equivalence(not first_event == second_event,
                       first_event != second_event)
