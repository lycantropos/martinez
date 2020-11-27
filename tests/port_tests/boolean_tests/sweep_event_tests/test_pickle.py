from hypothesis import given

from tests.port_tests.hints import PortedSweepEvent
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.sweep_events)
def test_round_trip(event: PortedSweepEvent) -> None:
    assert pickle_round_trip(event) == event
