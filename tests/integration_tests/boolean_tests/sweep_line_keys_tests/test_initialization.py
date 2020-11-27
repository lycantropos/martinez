from hypothesis import given

from tests.bind_tests.hints import BoundSweepLineKey
from tests.integration_tests.hints import BoundPortedSweepEventsPair
from tests.integration_tests.utils import (
    are_bound_ported_sweep_line_keys_equal)
from tests.port_tests.hints import PortedSweepLineKey
from . import strategies


@given(strategies.sweep_events_pairs)
def test_basic(events_pair: BoundPortedSweepEventsPair) -> None:
    bound_event, ported_event = events_pair

    bound = BoundSweepLineKey(bound_event)
    ported = PortedSweepLineKey(ported_event)

    assert are_bound_ported_sweep_line_keys_equal(bound, ported)
