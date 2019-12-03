from _martinez import (Contour,
                       Point)
from hypothesis import strategies

from tests.strategies import floats

points = strategies.builds(Point, floats, floats)
points_lists = strategies.lists(points)
non_negative_integers = strategies.integers(0, 65535)
non_negative_integers_lists = strategies.lists(non_negative_integers)
booleans = strategies.booleans()
contours = strategies.builds(Contour, points_lists,
                             non_negative_integers_lists, booleans)
