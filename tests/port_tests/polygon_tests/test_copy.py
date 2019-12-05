import copy

from hypothesis import given

from martinez.polygon import Polygon
from . import strategies


@given(strategies.polygons)
def test_shallow(polygon: Polygon) -> None:
    result = copy.copy(polygon)

    assert result is not polygon
    assert result == polygon
    assert result.contours is polygon.contours


@given(strategies.polygons)
def test_deep(polygon: Polygon) -> None:
    result = copy.deepcopy(polygon)

    assert result is not polygon
    assert result == polygon
    assert result.contours is not polygon.contours
