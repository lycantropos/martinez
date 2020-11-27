from hypothesis import given

from tests.bind_tests.hints import (BoundPolygon, Contour)
from tests.utils import capacity
from . import strategies


@given(strategies.polygons)
def test_basic(polygon: BoundPolygon) -> None:
    result = iter(polygon)

    assert all(isinstance(element, Contour)
               for element in result)


@given(strategies.polygons)
def test_elements(polygon: BoundPolygon) -> None:
    result = iter(polygon)

    assert all(element in polygon.contours
               for element in result)


@given(strategies.polygons)
def test_size(polygon: BoundPolygon) -> None:
    result = iter(polygon)

    assert capacity(result) == len(polygon.contours)
