from typing import (List,
                    Tuple)

from hypothesis import given

from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.operations_with_events_lists)
def test_basic(operation_with_events: Tuple[PortedOperation,
                                            List[PortedSweepEvent]]) -> None:
    operation, events = operation_with_events

    result = operation.process_events(events)

    assert result is None
