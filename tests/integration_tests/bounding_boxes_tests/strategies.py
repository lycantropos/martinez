from typing import Tuple

from _martinez import BoundingBox as Bound
from hypothesis import strategies

from martinez.bounding_box import BoundingBox as Ported
from tests.strategies import floats


def to_bound_with_ported_bounding_boxes(x_min: float, y_min: float,
                                        x_max: float, y_max: float
                                        ) -> Tuple[Bound, Ported]:
    return (Bound(x_min, y_min, x_max, y_max),
            Ported(x_min, y_min, x_max, y_max))


bounding_boxes_pairs = strategies.builds(to_bound_with_ported_bounding_boxes,
                                         floats, floats, floats, floats)
