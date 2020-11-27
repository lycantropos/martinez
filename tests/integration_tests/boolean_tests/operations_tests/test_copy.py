import copy
from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from tests.integration_tests.utils import are_bound_ported_operations_equal
from tests.port_tests.hints import PortedOperation
from . import strategies


@given(strategies.operations_pairs)
def test_shallow(operations_pair: Tuple[BoundOperation, PortedOperation]
                 ) -> None:
    bound, ported = operations_pair

    assert are_bound_ported_operations_equal(copy.copy(bound),
                                             copy.copy(ported))


@given(strategies.operations_pairs)
def test_deep(operations_pair: Tuple[BoundOperation, PortedOperation]) -> None:
    bound, ported = operations_pair

    assert are_bound_ported_operations_equal(copy.deepcopy(bound),
                                             copy.deepcopy(ported))
