from hypothesis import given

from martinez.polygon import Polygon
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.polygons)
def test_reflexivity(polygon: Polygon) -> None:
    assert polygon == polygon


@given(strategies.polygons, strategies.polygons)
def test_symmetry(first_polygon: Polygon, second_polygon: Polygon) -> None:
    assert equivalence(first_polygon == second_polygon,
                       second_polygon == first_polygon)


@given(strategies.polygons, strategies.polygons, strategies.polygons)
def test_transitivity(first_polygon: Polygon,
                      second_polygon: Polygon,
                      third_polygon: Polygon) -> None:
    assert implication(first_polygon == second_polygon
                       and second_polygon == third_polygon,
                       first_polygon == third_polygon)


@given(strategies.polygons, strategies.polygons)
def test_connection_with_inequality(first_polygon: Polygon,
                                    second_polygon: Polygon) -> None:
    assert equivalence(not first_polygon == second_polygon,
                       first_polygon != second_polygon)
