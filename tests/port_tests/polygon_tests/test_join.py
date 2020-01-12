import copy
from typing import Tuple

from hypothesis import given

from martinez.polygon import Polygon
from . import strategies


@given(strategies.polygons_pairs)
def test_basic(polygons_pair: Tuple[Polygon, Polygon]) -> None:
    first_polygon, second_polygon = polygons_pair

    result = first_polygon.join(second_polygon)

    assert result is None


@given(strategies.polygons_pairs)
def test_size(polygons_pair: Tuple[Polygon, Polygon]) -> None:
    first_polygon, second_polygon = polygons_pair

    original_first_polygon = copy.deepcopy(first_polygon)

    first_polygon.join(second_polygon)

    assert len(first_polygon.contours) == (len(original_first_polygon.contours)
                                           + len(second_polygon.contours))


@given(strategies.polygons_pairs)
def test_elements(polygons_pair: Tuple[Polygon, Polygon]) -> None:
    first_polygon, second_polygon = polygons_pair

    first_polygon.join(second_polygon)

    assert all(first_contour.points == second_contour.points
               for first_contour, second_contour
               in zip(first_polygon.contours[-len(second_polygon.contours):],
                      second_polygon.contours))
    assert all(first_contour.is_external is second_contour.is_external
               for first_contour, second_contour
               in zip(first_polygon.contours[-len(second_polygon.contours):],
                      second_polygon.contours))
