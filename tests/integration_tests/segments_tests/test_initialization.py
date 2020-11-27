from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import (BoundPoint,
                                    BoundSegment)
from tests.integration_tests.utils import are_bound_ported_points_equal
from tests.port_tests.hints import (PortedPoint,
                                    PortedSegment)
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs)
def test_basic(sources_pair: Tuple[BoundPoint, PortedPoint],
               targets_pair: Tuple[BoundPoint, PortedPoint]) -> None:
    bound_source, ported_source = sources_pair
    bound_target, ported_target = targets_pair

    bound, ported = (BoundSegment(bound_source, bound_target),
                     PortedSegment(ported_source, ported_target))

    assert are_bound_ported_points_equal(bound.source, ported.source)
    assert are_bound_ported_points_equal(bound.target, ported.target)
