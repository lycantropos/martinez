import pickle
from typing import Tuple

from _martinez import SweepEvent as Bound
from hypothesis import given

from martinez.boolean import SweepEvent as Ported
from tests.utils import are_bound_ported_sweep_events_equal
from . import strategies


@given(strategies.bound_with_ported_sweep_events_pairs)
def test_round_trip(bound_with_ported_sweep_events_pair: Tuple[Bound, Ported]
                    ) -> None:
    bound, ported = bound_with_ported_sweep_events_pair

    assert are_bound_ported_sweep_events_equal(
            pickle.loads(pickle.dumps(bound)),
            pickle.loads(pickle.dumps(ported)))
