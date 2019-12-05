from typing import List

from hypothesis import given

from martinez.contour import Contour
from martinez.polygon import Polygon
from . import strategies


@given(strategies.contours_lists)
def test_basic(contours: List[Contour]) -> None:
    result = Polygon(contours)

    assert result.contours == contours
