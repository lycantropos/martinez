from tests.port_tests.hints import PortedEdgeType

from tests.utils import all_unique


def test_basic():
    assert all_unique(PortedEdgeType.__members__.values())
