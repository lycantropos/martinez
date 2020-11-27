from hypothesis import given

from martinez import boolean
from tests.port_tests.hints import PortedSweepEvent
from . import strategies


@given(strategies.sweep_events)
def test_basic(event: PortedSweepEvent) -> None:
    result = repr(event)

    assert result.startswith(PortedSweepEvent.__qualname__)


@given(strategies.acyclic_sweep_events)
def test_round_trip(event: PortedSweepEvent) -> None:
    result = repr(event)

    scalar_type = type(event.point.x)
    assert eval(result, {**vars(boolean),
                         scalar_type.__qualname__: scalar_type}) == event
