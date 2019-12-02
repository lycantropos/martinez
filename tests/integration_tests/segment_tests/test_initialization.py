from typing import Tuple

from _martinez import (Point as BoundPoint,
                       Segment as Bound)
from hypothesis import given

from martinez.point import Point as PortedPoint
from martinez.segment import Segment as Ported
from tests.utils import are_bound_ported_points_equal
from . import strategies


@given(strategies.bound_with_ported_points_pairs,
       strategies.bound_with_ported_points_pairs)
def test_basic(bound_with_ported_sources_pair: Tuple[BoundPoint, PortedPoint],
               bound_with_ported_targets_pair: Tuple[BoundPoint, PortedPoint]
               ) -> None:
    bound_source, ported_source = bound_with_ported_sources_pair
    bound_target, ported_target = bound_with_ported_targets_pair

    bound, ported = (Bound(bound_source, bound_target),
                     Ported(ported_source, ported_target))

    assert are_bound_ported_points_equal(bound.source, ported.source)
    assert are_bound_ported_points_equal(bound.target, ported.target)
