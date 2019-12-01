from typing import Tuple

from _martinez import Point as Bounded
from hypothesis import strategies

from martinez.point import Point as Ported
from tests.strategies import floats


def to_bounded_with_ported_point(x: float, y: float) -> Tuple[Bounded, Ported]:
    return Bounded(x, y), Ported(x, y)


bounded_with_ported_points_pairs = strategies.builds(to_bounded_with_ported_point,
                                                     floats, floats)
