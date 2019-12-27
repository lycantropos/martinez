from typing import (List,
                    Tuple)

from _martinez import (Operation,
                       SweepEvent)
from hypothesis import given

from . import strategies


@given(strategies.non_empty_sweep_events_lists_with_indices_and_booleans_lists)
def test_basic(events_with_position_and_processed: Tuple[List[SweepEvent],
                                                         int, List[bool]]
               ) -> None:
    events, position, processed = events_with_position_and_processed

    result = Operation.to_next_position(position, events, processed)

    assert isinstance(result, int)


@given(strategies.non_empty_sweep_events_lists_with_indices_and_booleans_lists)
def test_properties(events_with_position_and_processed: Tuple[List[SweepEvent],
                                                              int, List[bool]]
                    ) -> None:
    events, position, processed = events_with_position_and_processed

    result = Operation.to_next_position(position, events, processed)

    assert result in range(len(events))
