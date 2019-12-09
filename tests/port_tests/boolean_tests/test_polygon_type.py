from martinez.boolean import PolygonType

from tests.utils import all_unique


def test_basic():
    assert all_unique(PolygonType.__members__.values())
