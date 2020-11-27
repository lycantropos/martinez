import sys

from hypothesis import given

from tests.bind_tests.hints import BoundContour as Contour
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = repr(contour)

    assert result.startswith(Contour.__module__)
    assert Contour.__qualname__ in result


@given(strategies.contours)
def test_round_trip(contour: Contour) -> None:
    result = repr(contour)

    assert eval(result, sys.modules) == contour
