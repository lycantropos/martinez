import copy

from hypothesis import given

from tests.bind_tests.hints import BoundPolygon
from . import strategies


@given(strategies.polygons)
def test_shallow(polygon: BoundPolygon) -> None:
    result = copy.copy(polygon)

    assert result is not polygon
    assert result == polygon


@given(strategies.polygons)
def test_deep(polygon: BoundPolygon) -> None:
    result = copy.deepcopy(polygon)

    assert result is not polygon
    assert result == polygon
