import sys

from hypothesis import given

from tests.bind_tests.hints import BoundPolygon
from . import strategies


@given(strategies.polygons)
def test_basic(polygon: BoundPolygon) -> None:
    result = repr(polygon)

    assert result.startswith(BoundPolygon.__module__)
    assert BoundPolygon.__qualname__ in result


@given(strategies.polygons)
def test_round_trip(polygon: BoundPolygon) -> None:
    result = repr(polygon)

    assert eval(result, sys.modules) == polygon
