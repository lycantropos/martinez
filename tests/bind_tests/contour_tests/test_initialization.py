from typing import List

from _martinez import (Contour,
                       Point)
from hypothesis import given

from . import strategies


@given(strategies.points_lists, strategies.non_negative_integers_lists,
       strategies.booleans)
def test_basic(points: List[Point],
               holes: List[int],
               is_external: bool) -> None:
    result = Contour(points, holes, is_external)

    assert result.points == points
    assert result.holes == holes
    assert result.is_external == is_external
