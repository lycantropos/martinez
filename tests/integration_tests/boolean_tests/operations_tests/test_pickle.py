from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from tests.integration_tests.utils import are_bound_ported_operations_equal
from tests.port_tests.hints import PortedOperation
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.operations_pairs)
def test_round_trip(operations_pair: Tuple[BoundOperation, PortedOperation]
                    ) -> None:
    bound, ported = operations_pair

    assert are_bound_ported_operations_equal(pickle_round_trip(bound),
                                             pickle_round_trip(ported))
