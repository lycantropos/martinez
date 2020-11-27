import copy
from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSegment
from tests.integration_tests.utils import are_bound_ported_segments_equal
from tests.port_tests.hints import PortedSegment
from . import strategies


@given(strategies.segments_pairs)
def test_shallow(segments_pair: Tuple[BoundSegment, PortedSegment]) -> None:
    bound, ported = segments_pair

    assert are_bound_ported_segments_equal(copy.copy(bound), copy.copy(ported))


@given(strategies.segments_pairs)
def test_deep(segments_pair: Tuple[BoundSegment, PortedSegment]) -> None:
    bound, ported = segments_pair

    assert are_bound_ported_segments_equal(copy.deepcopy(bound),
                                           copy.deepcopy(ported))
