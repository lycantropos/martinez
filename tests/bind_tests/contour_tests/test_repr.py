import sys

from hypothesis import given

from tests.bind_tests.hints import BoundContour
from . import strategies


@given(strategies.contours)
def test_basic(contour: BoundContour) -> None:
    result = repr(contour)

    assert result.startswith(BoundContour.__module__)
    assert BoundContour.__qualname__ in result


@given(strategies.contours)
def test_round_trip(contour: BoundContour) -> None:
    result = repr(contour)

    assert eval(result, sys.modules) == contour
