from _martinez import (BoundingBox,
                       Point)
from hypothesis import given

from tests.utils import equivalence
from . import strategies


@given(strategies.points)
def test_basic(point: Point) -> None:
    assert isinstance(point.bounding_box, BoundingBox)


@given(strategies.points, strategies.points)
def test_bijection(first_point: Point, second_point: Point) -> None:
    assert equivalence(first_point == second_point,
                       first_point.bounding_box == second_point.bounding_box)
