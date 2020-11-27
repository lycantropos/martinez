from tests.bind_tests.hints import BoundOperationType
from tests.port_tests.hints import PortedOperationType


def test_basic():
    assert BoundOperationType.__members__ == PortedOperationType.__members__
