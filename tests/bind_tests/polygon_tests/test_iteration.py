from _martinez import (Contour,
                       Polygon)
from hypothesis import given

from tests.utils import capacity
from . import strategies


@given(strategies.polygons)
def test_basic(polygon: Polygon) -> None:
    result = iter(polygon)

    assert all(isinstance(element, Contour)
               for element in result)


@given(strategies.polygons)
def test_elements(polygon: Polygon) -> None:
    result = iter(polygon)

    assert all(element in polygon.contours
               for element in result)


@given(strategies.polygons)
def test_size(polygon: Polygon) -> None:
    result = iter(polygon)

    assert capacity(result) == len(polygon.contours)
