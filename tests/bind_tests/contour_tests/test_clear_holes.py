from hypothesis import given

from tests.bind_tests.hints import BoundContour as Contour
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = contour.clear_holes()

    assert result is None


@given(strategies.contours)
def test_properties(contour: Contour) -> None:
    contour.clear_holes()

    assert not contour.holes
