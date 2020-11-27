from tests.bind_tests.hints import BoundPolygonType
from tests.port_tests.hints import PortedPolygonType


def test_basic():
    assert BoundPolygonType.__members__ == PortedPolygonType.__members__
