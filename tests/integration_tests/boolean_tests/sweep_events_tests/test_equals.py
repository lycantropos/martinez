from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from tests.port_tests.hints import PortedSweepEvent
from tests.utils import equivalence
from . import strategies


@given(strategies.sweep_events_pairs, strategies.sweep_events_pairs)
def test_basic(first_sweep_events_pair: Tuple[BoundSweepEvent,
                                              PortedSweepEvent],
               second_sweep_events_pair: Tuple[BoundSweepEvent,
                                               PortedSweepEvent]) -> None:
    first_bound, first_ported = first_sweep_events_pair
    second_bound, second_ported = second_sweep_events_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
