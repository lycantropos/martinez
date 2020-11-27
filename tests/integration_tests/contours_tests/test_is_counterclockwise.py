from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundContour
from tests.port_tests.hints import PortedContour
from . import strategies


@given(strategies.contours_pairs)
def test_basic(contours_pair: Tuple[BoundContour, PortedContour]) -> None:
    bound, ported = contours_pair

    assert bound.is_counterclockwise is ported.is_counterclockwise
