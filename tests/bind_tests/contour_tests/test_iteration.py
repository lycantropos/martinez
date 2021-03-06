from hypothesis import given

from tests.bind_tests.hints import (BoundContour,
                                    BoundPoint)
from tests.utils import capacity
from . import strategies


@given(strategies.contours)
def test_basic(contour: BoundContour) -> None:
    result = iter(contour)

    assert all(isinstance(element, BoundPoint)
               for element in result)


@given(strategies.contours)
def test_elements(contour: BoundContour) -> None:
    result = iter(contour)

    assert all(element in contour.points
               for element in result)


@given(strategies.contours)
def test_size(contour: BoundContour) -> None:
    result = iter(contour)

    assert capacity(result) == len(contour.points)
