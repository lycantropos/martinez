from _martinez import EdgeType as Bound

from martinez.boolean import EdgeType as Ported


def test_basic():
    assert Bound.__members__ == Ported.__members__
