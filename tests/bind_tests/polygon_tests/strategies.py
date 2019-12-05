from _martinez import (Contour,
                       Point,
                       Polygon)
from hypothesis import strategies

from tests.strategies import (booleans,
                              floats,
                              unsigned_integers,
                              unsigned_integers_lists)

booleans = booleans
non_negative_integers = unsigned_integers
non_negative_integers_lists = unsigned_integers_lists
points = strategies.builds(Point, floats, floats)
points_lists = strategies.lists(points)
contours = strategies.builds(Contour, points_lists,
                             non_negative_integers_lists, booleans)
contours_lists = strategies.lists(contours)
polygons = strategies.builds(Polygon, contours_lists)
