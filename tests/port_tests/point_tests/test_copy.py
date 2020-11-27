import copy

from hypothesis import given

from tests.port_tests.hints import PortedPoint
from . import strategies


@given(strategies.points)
def test_shallow(point: PortedPoint) -> None:
    result = copy.copy(point)

    assert result is not point
    assert result == point


@given(strategies.points)
def test_deep(point: PortedPoint) -> None:
    result = copy.deepcopy(point)

    assert result is not point
    assert result == point
