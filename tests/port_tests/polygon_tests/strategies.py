from hypothesis import strategies

from martinez.contour import Contour
from martinez.polygon import Polygon
from tests.strategies import (booleans,
                              non_negative_integers,
                              non_negative_integers_lists,
                              scalars_strategies,
                              scalars_to_ported_points,
                              scalars_to_ported_points_lists)
from tests.utils import MAX_CONTOURS_COUNT

booleans = booleans
non_negative_integers = non_negative_integers
non_negative_integers_lists = non_negative_integers_lists
points = scalars_strategies.flatmap(scalars_to_ported_points)
points_lists = scalars_strategies.flatmap(scalars_to_ported_points_lists)
contours = strategies.builds(Contour, points_lists,
                             non_negative_integers_lists, booleans)
contours_lists = strategies.lists(contours,
                                  max_size=MAX_CONTOURS_COUNT)
polygons = strategies.builds(Polygon, contours_lists)
