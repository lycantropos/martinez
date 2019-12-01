from typing import Tuple

from _martinez import Point as Bound
from hypothesis import strategies

from martinez.point import Point as Ported
from tests.strategies import floats

floats = floats


def to_bound_with_ported_point(x: float, y: float) -> Tuple[Bound, Ported]:
    return Bound(x, y), Ported(x, y)


bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_point, floats, floats)
