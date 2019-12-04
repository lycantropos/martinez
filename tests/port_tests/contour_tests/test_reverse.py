from copy import deepcopy

from hypothesis import given

from martinez.contour import Contour
from tests.utils import equivalence
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = contour.reverse()

    assert result is None


@given(strategies.contours)
def test_involution(contour: Contour) -> None:
    original = deepcopy(contour)

    contour.reverse()
    contour.reverse()

    assert contour == original


@given(strategies.contours)
def test_orientation(contour: Contour) -> None:
    original = deepcopy(contour)

    contour.reverse()

    assert equivalence(len(contour.points) <= 1,
                       contour.is_counterclockwise
                       is original.is_counterclockwise)
