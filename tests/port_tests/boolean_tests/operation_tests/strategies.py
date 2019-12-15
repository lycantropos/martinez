from hypothesis import strategies

from martinez.boolean import OperationType
from martinez.contour import Contour
from martinez.polygon import Polygon
from tests.strategies import (booleans, scalars_strategies,
                              scalars_to_ported_points_triplets,
                              unsigned_integers_lists)
from tests.utils import vertices_form_strict_polygon

operations_types = strategies.sampled_from(list(OperationType.__members__
                                                .values()))
triangles_vertices = (scalars_strategies
                      .flatmap(scalars_to_ported_points_triplets)
                      .filter(vertices_form_strict_polygon))
contours_vertices = triangles_vertices
contours = strategies.builds(Contour, contours_vertices,
                             unsigned_integers_lists, booleans)
contours_lists = strategies.lists(contours)
empty_contours_lists = strategies.builds(list)
non_empty_contours_lists = strategies.lists(contours,
                                            min_size=1)
polygons = strategies.builds(Polygon, contours_lists)
empty_polygons = strategies.builds(Polygon, empty_contours_lists)
non_empty_polygons = strategies.builds(Polygon, contours_lists)
