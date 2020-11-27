from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSegment
from tests.integration_tests.utils import are_bound_ported_segments_equal
from tests.port_tests.hints import PortedSegment
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.segments_pairs)
def test_round_trip(segments_pair: Tuple[BoundSegment, PortedSegment]) -> None:
    bound, ported = segments_pair

    assert are_bound_ported_segments_equal(pickle_round_trip(bound),
                                           pickle_round_trip(ported))
