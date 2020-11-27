from tests.bind_tests.hints import BoundPolygonType

from tests.utils import all_unique


def test_basic():
    assert all_unique(BoundPolygonType.__members__.values())
