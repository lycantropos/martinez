from typing import Tuple

from _martinez import Operation as Bound
from hypothesis import given

from martinez.boolean import Operation as Ported
from tests.utils import (pickle_round_trip)
from ...utils import are_bound_ported_operations_equal
from . import strategies


@given(strategies.operations_pairs)
def test_round_trip(operations_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = operations_pair

    assert are_bound_ported_operations_equal(pickle_round_trip(bound),
                                             pickle_round_trip(ported))
