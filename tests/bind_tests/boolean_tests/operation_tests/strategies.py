from _martinez import (Contour,
                       Operation,
                       Point,
                       Polygon)
from hypothesis import strategies

from tests.strategies import (booleans,
                              bound_operations_types,
                              floats,
                              unsigned_integers_lists)
from tests.utils import vertices_form_strict_polygon

operations_types = bound_operations_types
triangles_vertices = (strategies.lists(strategies.builds(Point,
                                                         floats, floats),
                                       min_size=3,
                                       max_size=3)
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
operations = strategies.builds(Operation, polygons, polygons, operations_types)
