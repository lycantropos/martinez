from typing import List

from hypothesis import given

from tests.bind_tests.hints import (BoundPolygon, Contour)
from . import strategies


@given(strategies.contours_lists)
def test_basic(contours: List[Contour]) -> None:
    result = BoundPolygon(contours)

    assert result.contours == contours
