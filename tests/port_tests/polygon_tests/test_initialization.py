from typing import List

from hypothesis import given

from tests.port_tests.hints import (PortedContour,
                                    PortedPolygon)
from . import strategies


@given(strategies.contours_lists)
def test_basic(contours: List[PortedContour]) -> None:
    result = PortedPolygon(contours)

    assert result.contours == contours
