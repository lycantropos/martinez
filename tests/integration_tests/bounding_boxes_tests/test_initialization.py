from hypothesis import given

from tests.bind_tests.hints import BoundBoundingBox
from tests.integration_tests.utils import are_bound_ported_bounding_boxes_equal
from tests.port_tests.hints import PortedBoundingBox
from . import strategies


@given(strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_basic(x_min: float, y_min: float, x_max: float, y_max: float) -> None:
    bound, ported = (BoundBoundingBox(x_min, y_min, x_max, y_max),
                     PortedBoundingBox(x_min, y_min, x_max, y_max))

    assert are_bound_ported_bounding_boxes_equal(bound, ported)
