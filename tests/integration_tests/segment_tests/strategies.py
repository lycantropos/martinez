from typing import Tuple

from _martinez import (Point as BoundPoint,
                       Segment as Bound)
from hypothesis import strategies

from martinez.point import Point as PortedPoint
from martinez.segment import Segment as Ported
from tests.strategies import floats
from tests.strategies.factories import to_bound_with_ported_points_pair

floats = floats
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)


def to_bound_with_ported_segments_pair(
        bound_with_ported_sources_pair: Tuple[BoundPoint, PortedPoint],
        bound_with_ported_targets_pair: Tuple[BoundPoint, PortedPoint]
) -> Tuple[Bound, Ported]:
    bound_source, ported_source = bound_with_ported_sources_pair
    bound_target, ported_target = bound_with_ported_targets_pair

    return (Bound(bound_source, bound_target),
            Ported(ported_source, ported_target))


bound_with_ported_segments_pairs = strategies.builds(
        to_bound_with_ported_segments_pair,
        bound_with_ported_points_pairs, bound_with_ported_points_pairs)
