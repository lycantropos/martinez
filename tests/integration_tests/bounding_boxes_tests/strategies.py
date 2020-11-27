from typing import Tuple

from hypothesis import strategies

from tests.bind_tests.hints import BoundBoundingBox
from tests.port_tests.hints import PortedBoundingBox
from tests.strategies import floats


def to_bound_with_ported_bounding_boxes(x_min: float, y_min: float,
                                        x_max: float, y_max: float
                                        ) -> Tuple[BoundBoundingBox,
                                                   PortedBoundingBox]:
    return (BoundBoundingBox(x_min, y_min, x_max, y_max),
            PortedBoundingBox(x_min, y_min, x_max, y_max))


bounding_boxes_pairs = strategies.builds(to_bound_with_ported_bounding_boxes,
                                         floats, floats, floats, floats)
