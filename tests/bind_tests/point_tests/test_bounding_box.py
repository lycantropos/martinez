from hypothesis import given

from tests.bind_tests.hints import (BoundBoundingBox,
                                    BoundPoint)
from tests.utils import equivalence
from . import strategies


@given(strategies.points)
def test_basic(point: BoundPoint) -> None:
    assert isinstance(point.bounding_box, BoundBoundingBox)


@given(strategies.points, strategies.points)
def test_bijection(first_point: BoundPoint, second_point: BoundPoint) -> None:
    assert equivalence(first_point == second_point,
                       first_point.bounding_box == second_point.bounding_box)
