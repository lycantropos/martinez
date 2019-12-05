from hypothesis import strategies

from martinez.contour import Contour
from tests.strategies import (booleans,
                              non_negative_integers,
                              non_negative_integers_lists,
                              scalars_strategies,
                              scalars_to_ported_points)

booleans = booleans
non_negative_integers = non_negative_integers
non_negative_integers_lists = non_negative_integers_lists
points = scalars_strategies.flatmap(scalars_to_ported_points)
points_lists = strategies.lists(points)
contours = strategies.builds(Contour, points_lists,
                             non_negative_integers_lists, booleans)
contours_lists = strategies.lists(contours)