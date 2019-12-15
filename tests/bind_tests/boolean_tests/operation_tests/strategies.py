from typing import List

from _martinez import (Contour,
                       OperationType,
                       Point,
                       Polygon,
                       sign)
from hypothesis import strategies

from tests.strategies import (booleans,
                              floats,
                              unsigned_integers_lists)

operations_types = strategies.sampled_from(list(OperationType.__members__
                                                .values()))


def vertices_forms_strict_polygon(vertices: List[Point]) -> bool:
    return all(sign(vertices[index - 1],
                    vertices[index],
                    vertices[(index + 1) % len(vertices)])
               for index in range(len(vertices)))


triangles_vertices = (strategies.lists(strategies.builds(Point,
                                                         floats, floats),
                                       min_size=3,
                                       max_size=3)
                      .filter(vertices_forms_strict_polygon))
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
