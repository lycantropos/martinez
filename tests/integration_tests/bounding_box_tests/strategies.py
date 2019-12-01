from typing import Tuple

from _martinez import BoundingBox as Bounded
from hypothesis import strategies

from martinez.bounding_box import BoundingBox as Ported
from tests.strategies import floats


def to_bounded_with_ported_bounding_boxes(x_min: float, y_min: float,
                                          x_max: float, y_max: float
                                          ) -> Tuple[Bounded, Ported]:
    return (Bounded(x_min, y_min, x_max, y_max),
            Ported(x_min, y_min, x_max, y_max))


bounded_with_ported_bounding_boxes_pairs = strategies.builds(
        to_bounded_with_ported_bounding_boxes, floats, floats, floats, floats)
