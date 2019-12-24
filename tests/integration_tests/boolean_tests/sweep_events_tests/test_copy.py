import copy
from typing import Tuple

from _martinez import SweepEvent as Bound
from hypothesis import given

from martinez.boolean import SweepEvent as Ported
from tests.utils import are_bound_ported_sweep_events_equal
from . import strategies


@given(strategies.sweep_events_pairs)
def test_shallow(sweep_events_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = sweep_events_pair

    assert are_bound_ported_sweep_events_equal(copy.copy(bound),
                                               copy.copy(ported))


@given(strategies.sweep_events_pairs)
def test_deep(sweep_events_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = sweep_events_pair

    assert are_bound_ported_sweep_events_equal(copy.deepcopy(bound),
                                               copy.deepcopy(ported))
