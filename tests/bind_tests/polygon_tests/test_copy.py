import copy

from _martinez import Polygon
from hypothesis import given

from . import strategies


@given(strategies.polygons)
def test_shallow(polygon: Polygon) -> None:
    result = copy.copy(polygon)

    assert result is not polygon
    assert result == polygon


@given(strategies.polygons)
def test_deep(polygon: Polygon) -> None:
    result = copy.deepcopy(polygon)

    assert result is not polygon
    assert result == polygon
