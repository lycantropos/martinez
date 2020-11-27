from hypothesis import given

from tests.port_tests.hints import (PortedContour,
                                    PortedPolygon)
from tests.utils import capacity
from . import strategies


@given(strategies.polygons)
def test_basic(polygon: PortedPolygon) -> None:
    result = iter(polygon)

    assert all(isinstance(element, PortedContour) for element in result)


@given(strategies.polygons)
def test_elements(polygon: PortedPolygon) -> None:
    result = iter(polygon)

    assert all(element in polygon.contours for element in result)


@given(strategies.polygons)
def test_size(polygon: PortedPolygon) -> None:
    result = iter(polygon)

    assert capacity(result) == len(polygon.contours)
