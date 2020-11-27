from typing import List

from hypothesis import given

from tests.bind_tests.hints import (BoundContour,
                                    BoundPolygon)
from . import strategies


@given(strategies.contours_lists)
def test_basic(contours: List[BoundContour]) -> None:
    result = BoundPolygon(contours)

    assert result.contours == contours
