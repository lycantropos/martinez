from typing import List

from _martinez import (Contour,
                       Polygon)
from hypothesis import given

from . import strategies


@given(strategies.contours_lists)
def test_basic(contours: List[Contour]) -> None:
    result = Polygon(contours)

    assert result.contours == contours
