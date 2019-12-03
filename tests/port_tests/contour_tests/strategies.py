from hypothesis import strategies

from martinez.contour import Contour
from tests.strategies import (scalars_strategies,
                              scalars_to_ported_points)

points = scalars_strategies.flatmap(scalars_to_ported_points)
points_lists = strategies.lists(points)
non_negative_integers_lists = strategies.lists(strategies.integers(0))
booleans = strategies.booleans()
contours = strategies.builds(Contour, points_lists,
                             non_negative_integers_lists, booleans)
