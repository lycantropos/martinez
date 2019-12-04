import copy

from _martinez import Contour
from hypothesis import given

from tests.utils import equivalence
from . import strategies


@given(strategies.contours, strategies.floats, strategies.floats)
def test_basic(contour: Contour, x: float, y: float) -> None:
    result = contour.move(x, y)

    assert result is None


@given(strategies.contours, strategies.floats, strategies.floats)
def test_properties(contour: Contour, x: float, y: float) -> None:
    original = copy.deepcopy(contour)

    contour.move(x, y)

    assert equivalence(original == contour, not contour.points or not (x or y))
