from hypothesis import strategies

from tests.bind_tests.hints import (BoundContour,
                                    BoundPoint)
from tests.strategies import (booleans,
                              floats,
                              unsigned_integers,
                              unsigned_integers_lists)

booleans = booleans
non_negative_integers = unsigned_integers
non_negative_integers_lists = unsigned_integers_lists
points = strategies.builds(BoundPoint, floats, floats)
points_lists = strategies.lists(points)
contours = strategies.builds(BoundContour, points_lists,
                             non_negative_integers_lists, booleans)
