from _martinez import PolygonType as Bound

from martinez.boolean import PolygonType as Ported


def test_basic():
    assert Bound.__members__ == Ported.__members__
