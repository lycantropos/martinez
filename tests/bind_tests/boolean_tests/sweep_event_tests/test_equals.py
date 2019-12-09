from _martinez import SweepEvent
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.sweep_events)
def test_reflexivity(sweep_event: SweepEvent) -> None:
    assert sweep_event == sweep_event


@given(strategies.sweep_events, strategies.sweep_events)
def test_symmetry(first_sweep_event: SweepEvent,
                  second_sweep_event: SweepEvent) -> None:
    assert equivalence(first_sweep_event == second_sweep_event,
                       second_sweep_event == first_sweep_event)


@given(strategies.sweep_events, strategies.sweep_events,
       strategies.sweep_events)
def test_transitivity(first_sweep_event: SweepEvent,
                      second_sweep_event: SweepEvent,
                      third_sweep_event: SweepEvent) -> None:
    assert implication(first_sweep_event == second_sweep_event
                       and second_sweep_event == third_sweep_event,
                       first_sweep_event == third_sweep_event)


@given(strategies.sweep_events, strategies.sweep_events)
def test_connection_with_inequality(first_sweep_event: SweepEvent,
                                    second_sweep_event: SweepEvent) -> None:
    assert equivalence(not first_sweep_event == second_sweep_event,
                       first_sweep_event != second_sweep_event)
