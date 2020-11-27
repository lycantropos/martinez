from typing import List

from hypothesis import given

from tests.port_tests.hints import (PortedContour,
                                    PortedPoint)
from . import strategies


@given(strategies.points_lists, strategies.non_negative_integers_lists,
       strategies.booleans)
def test_basic(points: List[PortedPoint],
               holes: List[int],
               is_external: bool) -> None:
    result = PortedContour(points, holes, is_external)

    assert result.points == points
    assert result.holes == holes
    assert result.is_external == is_external
