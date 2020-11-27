from typing import Tuple

from _martinez import Contour as Bound
from hypothesis import given

from martinez.contour import Contour as Ported
from tests.utils import (pickle_round_trip)
from ..utils import are_bound_ported_contours_equal
from . import strategies


@given(strategies.contours_pairs)
def test_round_trip(contours_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = contours_pair

    assert are_bound_ported_contours_equal(pickle_round_trip(bound),
                                           pickle_round_trip(ported))
