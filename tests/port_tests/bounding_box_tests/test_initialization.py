from typing import Tuple

from hypothesis import given

from martinez.bounding_box import BoundingBox
from martinez.hints import Scalar
from . import strategies


@given(strategies.scalars_quadruples)
def test_basic(scalars_quadruple: Tuple[Scalar, Scalar, Scalar, Scalar]
               ) -> None:
    x_min, y_min, x_max, y_max = scalars_quadruple

    result = BoundingBox(x_min, y_min, x_max, y_max)

    assert result.x_min == x_min
    assert result.y_min == y_min
    assert result.x_max == x_max
    assert result.y_max == y_max
