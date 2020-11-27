from hypothesis import given

from tests.port_tests.hints import PortedContour
from . import strategies


@given(strategies.contours)
def test_basic(contour: PortedContour) -> None:
    result = contour.set_counterclockwise()

    assert result is None
