from typing import List

from hypothesis import given

from tests.bind_tests.hints import (BoundContour,
                                    BoundPoint)
from . import strategies


@given(strategies.points_lists, strategies.non_negative_integers_lists,
       strategies.booleans)
def test_basic(points: List[BoundPoint],
               holes: List[int],
               is_external: bool) -> None:
    result = BoundContour(points, holes, is_external)

    assert result.points == points
    assert result.holes == holes
    assert result.is_external == is_external
