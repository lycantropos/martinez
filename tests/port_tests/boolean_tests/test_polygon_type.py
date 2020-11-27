from tests.port_tests.hints import PortedPolygonType

from tests.utils import all_unique


def test_basic():
    assert all_unique(PortedPolygonType.__members__.values())
