from typing import Tuple

from hypothesis import given

from martinez.boolean import SweepEvent
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.sweep_events)
def test_reflexivity(event: SweepEvent) -> None:
    assert event == event


@given(strategies.sweep_events_pairs)
def test_symmetry(events_pair: Tuple[SweepEvent, SweepEvent]) -> None:
    first_event, second_event = events_pair

    assert equivalence(first_event == second_event,
                       second_event == first_event)


@given(strategies.sweep_events_triplets)
def test_transitivity(events_triplet: Tuple[SweepEvent, SweepEvent, SweepEvent]
                      ) -> None:
    first_event, second_event, third_event = events_triplet

    assert implication(first_event == second_event
                       and second_event == third_event,
                       first_event == third_event)


@given(strategies.sweep_events_pairs)
def test_connection_with_inequality(events_pair: Tuple[SweepEvent, SweepEvent]
                                    ) -> None:
    first_event, second_event = events_pair

    assert equivalence(not first_event == second_event,
                       first_event != second_event)
