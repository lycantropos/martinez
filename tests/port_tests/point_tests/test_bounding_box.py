from hypothesis import given

from tests.port_tests.hints import (PortedBoundingBox,
                                    PortedPoint)
from tests.utils import equivalence
from . import strategies


@given(strategies.points)
def test_basic(point: PortedPoint) -> None:
    assert isinstance(point.bounding_box, PortedBoundingBox)


@given(strategies.points, strategies.points)
def test_bijection(first_point: PortedPoint,
                   second_point: PortedPoint) -> None:
    assert equivalence(first_point == second_point,
                       first_point.bounding_box == second_point.bounding_box)
