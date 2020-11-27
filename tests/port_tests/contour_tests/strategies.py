from tests.strategies import (booleans,
                              non_negative_integers,
                              non_negative_integers_lists,
                              scalars_strategies)
from tests.port_tests.factories import scalars_to_ported_contours, \
    scalars_to_ported_points, \
    scalars_to_ported_points_lists
from tests.utils import (identity,
                         to_pairs,
                         to_triplets)

booleans = booleans
non_negative_integers = non_negative_integers
non_negative_integers_lists = non_negative_integers_lists
points = scalars_strategies.flatmap(scalars_to_ported_points)
points_lists = scalars_strategies.flatmap(scalars_to_ported_points_lists)
contours_strategies = scalars_strategies.map(scalars_to_ported_contours)
contours = contours_strategies.flatmap(identity)
contours_pairs = contours_strategies.flatmap(to_pairs)
contours_triplets = contours_strategies.flatmap(to_triplets)
