from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from tests.port_tests.hints import PortedOperation
from tests.utils import equivalence
from . import strategies


@given(strategies.operations_pairs, strategies.operations_pairs)
def test_basic(first_operations_pair: Tuple[BoundOperation, PortedOperation],
               second_operations_pair: Tuple[BoundOperation, PortedOperation]
               ) -> None:
    first_bound, first_ported = first_operations_pair
    second_bound, second_ported = second_operations_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
