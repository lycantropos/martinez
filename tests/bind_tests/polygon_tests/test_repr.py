import sys

from _martinez import Polygon
from hypothesis import given

from . import strategies


@given(strategies.polygons)
def test_basic(polygon: Polygon) -> None:
    result = repr(polygon)

    assert result.startswith(Polygon.__module__)
    assert Polygon.__qualname__ in result


@given(strategies.polygons)
def test_round_trip(polygon: Polygon) -> None:
    result = repr(polygon)

    assert eval(result, sys.modules) == polygon
