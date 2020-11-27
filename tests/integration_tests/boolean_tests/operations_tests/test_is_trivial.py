from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from tests.integration_tests.utils import are_bound_ported_polygons_equal
from tests.port_tests.hints import PortedOperation
from . import strategies


@given(strategies.operations_pairs)
def test_basic(operations_pair: Tuple[BoundOperation, PortedOperation]
               ) -> None:
    bound, ported = operations_pair

    assert bound.is_trivial is ported.is_trivial
    assert are_bound_ported_polygons_equal(bound.resultant, ported.resultant)
