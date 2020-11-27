from tests.bind_tests.hints import BoundEdgeType
from tests.port_tests.hints import PortedEdgeType


def test_basic():
    assert BoundEdgeType.__members__ == PortedEdgeType.__members__
