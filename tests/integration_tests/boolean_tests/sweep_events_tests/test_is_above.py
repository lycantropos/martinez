from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import (BoundPoint,
                                    BoundSweepEvent)
from tests.port_tests.hints import (PortedPoint,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.nested_sweep_events_pairs,
       strategies.points_pairs)
def test_basic(sweep_events_pair: Tuple[BoundSweepEvent, PortedSweepEvent],
               points_pair: Tuple[BoundPoint, PortedPoint]) -> None:
    bound, ported = sweep_events_pair
    bound_point, ported_point = points_pair

    assert bound.is_above(bound_point) is ported.is_above(ported_point)
