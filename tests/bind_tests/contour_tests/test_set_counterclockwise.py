from hypothesis import given

from tests.bind_tests.hints import BoundContour as Contour
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = contour.set_counterclockwise()

    assert result is None
