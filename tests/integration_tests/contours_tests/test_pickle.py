import pickle
from typing import Tuple

from _martinez import Contour as Bound
from hypothesis import given

from martinez.contour import Contour as Ported
from tests.utils import are_bound_ported_contours_equal
from . import strategies


@given(strategies.bound_with_ported_contours_pairs)
def test_round_trip(bound_with_ported_contours_pair: Tuple[Bound, Ported]
                    ) -> None:
    bound, ported = bound_with_ported_contours_pair

    assert are_bound_ported_contours_equal(pickle.loads(pickle.dumps(bound)),
                                           pickle.loads(pickle.dumps(ported)))
