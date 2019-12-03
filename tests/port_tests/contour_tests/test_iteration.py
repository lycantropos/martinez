from hypothesis import given

from martinez.contour import Contour
from martinez.point import Point
from tests.utils import capacity
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = iter(contour)

    assert all(isinstance(element, Point)
               for element in result)


@given(strategies.contours)
def test_elements(contour: Contour) -> None:
    result = iter(contour)

    assert all(element in contour.points
               for element in result)


@given(strategies.contours)
def test_size(contour: Contour) -> None:
    result = iter(contour)

    assert capacity(result) == len(contour.points)
