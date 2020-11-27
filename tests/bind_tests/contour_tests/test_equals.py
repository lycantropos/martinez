from hypothesis import given

from tests.bind_tests.hints import BoundContour
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.contours)
def test_reflexivity(contour: BoundContour) -> None:
    assert contour == contour


@given(strategies.contours, strategies.contours)
def test_symmetry(first_contour: BoundContour,
                  second_contour: BoundContour) -> None:
    assert equivalence(first_contour == second_contour,
                       second_contour == first_contour)


@given(strategies.contours, strategies.contours, strategies.contours)
def test_transitivity(first_contour: BoundContour,
                      second_contour: BoundContour,
                      third_contour: BoundContour) -> None:
    assert implication(first_contour == second_contour
                       and second_contour == third_contour,
                       first_contour == third_contour)


@given(strategies.contours, strategies.contours)
def test_connection_with_inequality(first_contour: BoundContour,
                                    second_contour: BoundContour) -> None:
    assert equivalence(not first_contour == second_contour,
                       first_contour != second_contour)
