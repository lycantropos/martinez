from typing import Tuple

from hypothesis import given

from tests.port_tests.hints import PortedPoint
from tests.utils import Scalar
from . import strategies


@given(strategies.scalars_pairs)
def test_basic(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    x, y = scalars_pair

    result = PortedPoint(x, y)

    assert result.x == x
    assert result.y == y
