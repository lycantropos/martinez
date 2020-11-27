import copy

from hypothesis import given

from tests.bind_tests.hints import BoundPoint as BoundPoint
from . import strategies


@given(strategies.points)
def test_shallow(point: BoundPoint) -> None:
    result = copy.copy(point)

    assert result is not point
    assert result == point


@given(strategies.points)
def test_deep(point: BoundPoint) -> None:
    result = copy.deepcopy(point)

    assert result is not point
    assert result == point
