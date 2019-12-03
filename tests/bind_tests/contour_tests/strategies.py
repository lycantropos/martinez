from _martinez import (Contour,
                       Point)
from hypothesis import strategies

from tests.strategies import floats

points_lists = strategies.lists(strategies.builds(Point, floats, floats))
non_negative_integers_lists = strategies.lists(strategies.integers(0, 65535))
booleans = strategies.booleans()
contours = strategies.builds(Contour, points_lists,
                             non_negative_integers_lists, booleans)
