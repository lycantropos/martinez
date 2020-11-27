from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSegment
from tests.integration_tests.utils import are_bound_ported_points_equal
from tests.port_tests.hints import PortedSegment
from . import strategies


@given(strategies.segments_pairs)
def test_basic(segments_pair: Tuple[BoundSegment, PortedSegment]) -> None:
    bound, ported = segments_pair

    assert are_bound_ported_points_equal(bound.max, ported.max)
