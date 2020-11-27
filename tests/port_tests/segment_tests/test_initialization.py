from typing import Tuple

from hypothesis import given

from tests.port_tests.hints import (PortedPoint,
                                    PortedSegment)
from . import strategies


@given(strategies.points_pairs)
def test_basic(points_pair: Tuple[PortedPoint, PortedPoint]) -> None:
    source, target = points_pair

    result = PortedSegment(source, target)

    assert result.source == source
    assert result.target == target
