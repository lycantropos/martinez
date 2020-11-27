from hypothesis import given

from tests.bind_tests.hints import BoundPolygon as BoundPolygon
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.polygons)
def test_reflexivity(polygon: BoundPolygon) -> None:
    assert polygon == polygon


@given(strategies.polygons, strategies.polygons)
def test_symmetry(first_polygon: BoundPolygon,
                  second_polygon: BoundPolygon) -> None:
    assert equivalence(first_polygon == second_polygon,
                       second_polygon == first_polygon)


@given(strategies.polygons, strategies.polygons, strategies.polygons)
def test_transitivity(first_polygon: BoundPolygon,
                      second_polygon: BoundPolygon,
                      third_polygon: BoundPolygon) -> None:
    assert implication(first_polygon == second_polygon
                       and second_polygon == third_polygon,
                       first_polygon == third_polygon)


@given(strategies.polygons, strategies.polygons)
def test_connection_with_inequality(first_polygon: BoundPolygon,
                                    second_polygon: BoundPolygon) -> None:
    assert equivalence(not first_polygon == second_polygon,
                       first_polygon != second_polygon)
