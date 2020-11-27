from hypothesis import given

from tests.bind_tests.hints import BoundContour
from . import strategies


@given(strategies.contours)
def test_basic(contour: BoundContour) -> None:
    result = contour.clear_holes()

    assert result is None


@given(strategies.contours)
def test_properties(contour: BoundContour) -> None:
    contour.clear_holes()

    assert not contour.holes
