from hypothesis import strategies

from tests.strategies import (floats)
from tests.integration_tests.factories import to_bound_with_ported_points_pair

floats = floats
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
