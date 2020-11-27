from hypothesis import given

from tests.port_tests.hints import PortedPoint
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.points)
def test_reflexivity(point: PortedPoint) -> None:
    assert point == point


@given(strategies.points, strategies.points)
def test_symmetry(first_point: PortedPoint,
                  second_point: PortedPoint) -> None:
    assert equivalence(first_point == second_point,
                       second_point == first_point)


@given(strategies.points, strategies.points, strategies.points)
def test_transitivity(first_point: PortedPoint, second_point: PortedPoint,
                      third_point: PortedPoint) -> None:
    assert implication(first_point == second_point
                       and second_point == third_point,
                       first_point == third_point)


@given(strategies.points, strategies.points)
def test_connection_with_inequality(first_point: PortedPoint,
                                    second_point: PortedPoint) -> None:
    assert equivalence(not first_point == second_point,
                       first_point != second_point)
