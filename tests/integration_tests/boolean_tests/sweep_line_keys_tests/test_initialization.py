from _martinez import SweepLineKey as BoundSweepLineKey
from hypothesis import given

from martinez.boolean import SweepLineKey as PortedSweepLineKey
from tests.utils import (BoundPortedSweepEventsPair,
                         are_bound_ported_sweep_line_keys_equal)
from . import strategies


@given(strategies.sweep_events_pairs)
def test_basic(events_pair: BoundPortedSweepEventsPair) -> None:
    bound_event, ported_event = events_pair

    bound = BoundSweepLineKey(bound_event)
    ported = PortedSweepLineKey(ported_event)

    assert are_bound_ported_sweep_line_keys_equal(bound, ported)
