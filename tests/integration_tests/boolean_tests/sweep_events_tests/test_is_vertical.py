from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from tests.port_tests.hints import PortedSweepEvent
from . import strategies


@given(strategies.nested_sweep_events_pairs)
def test_basic(sweep_events_pair: Tuple[BoundSweepEvent, PortedSweepEvent]
               ) -> None:
    bound, ported = sweep_events_pair

    assert bound.is_vertical is ported.is_vertical
