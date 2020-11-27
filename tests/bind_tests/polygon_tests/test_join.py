import copy

from hypothesis import given

from tests.bind_tests.hints import BoundPolygon
from . import strategies


@given(strategies.polygons, strategies.polygons)
def test_basic(first_polygon: BoundPolygon,
               second_polygon: BoundPolygon) -> None:
    result = first_polygon.join(second_polygon)

    assert result is None


@given(strategies.polygons, strategies.polygons)
def test_size(first_polygon: BoundPolygon,
              second_polygon: BoundPolygon) -> None:
    original_first_polygon = copy.deepcopy(first_polygon)

    first_polygon.join(second_polygon)

    assert len(first_polygon.contours) == (len(original_first_polygon.contours)
                                           + len(second_polygon.contours))


@given(strategies.polygons, strategies.polygons)
def test_elements(first_polygon: BoundPolygon,
                  second_polygon: BoundPolygon) -> None:
    first_polygon.join(second_polygon)

    assert all(first_contour.points == second_contour.points
               for first_contour, second_contour
               in zip(first_polygon.contours[-len(second_polygon.contours):],
                      second_polygon.contours))
    assert all(first_contour.is_external is second_contour.is_external
               for first_contour, second_contour
               in zip(first_polygon.contours[-len(second_polygon.contours):],
                      second_polygon.contours))
