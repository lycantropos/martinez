import copy
from typing import Tuple

from _martinez import Operation as Bound
from hypothesis import given

from martinez.boolean import Operation as Ported
from tests.utils import are_bound_ported_operations_equal
from . import strategies


@given(strategies.operations_pairs)
def test_shallow(operations_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = operations_pair

    assert are_bound_ported_operations_equal(copy.copy(bound),
                                             copy.copy(ported))


@given(strategies.operations_pairs)
def test_deep(operations_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = operations_pair

    assert are_bound_ported_operations_equal(copy.deepcopy(bound),
                                             copy.deepcopy(ported))
