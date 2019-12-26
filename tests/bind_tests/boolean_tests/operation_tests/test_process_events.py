from typing import (List,
                    Tuple)

from _martinez import (Operation,
                       SweepEvent)
from hypothesis import given

from tests.utils import implication
from . import strategies


@given(strategies.operations_with_events_lists)
def test_basic(operation_with_events: Tuple[Operation, List[SweepEvent]]
               ) -> None:
    operation, events = operation_with_events

    result = operation.process_events(events)

    assert result is None


@given(strategies.operations_with_events_lists)
def test_properties(operation_with_events: Tuple[Operation, List[SweepEvent]]
                    ) -> None:
    operation, events = operation_with_events

    operation.process_events(events)

    assert implication(bool(events), bool(operation.resultant.contours))
