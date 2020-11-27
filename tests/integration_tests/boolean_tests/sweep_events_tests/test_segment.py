from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from tests.integration_tests.utils import are_bound_ported_segments_equal
from tests.port_tests.hints import PortedSweepEvent
from . import strategies


@given(strategies.nested_sweep_events_pairs)
def test_basic(sweep_events_pair: Tuple[BoundSweepEvent, PortedSweepEvent]
               ) -> None:
    bound, ported = sweep_events_pair

    assert are_bound_ported_segments_equal(bound.segment, ported.segment)
