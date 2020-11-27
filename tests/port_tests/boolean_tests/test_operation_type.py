from tests.port_tests.hints import PortedOperationType

from tests.utils import all_unique


def test_basic():
    assert all_unique(PortedOperationType.__members__.values())
