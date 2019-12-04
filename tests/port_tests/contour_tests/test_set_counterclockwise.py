from hypothesis import given

from martinez.contour import Contour
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = contour.set_counterclockwise()

    assert result is None
