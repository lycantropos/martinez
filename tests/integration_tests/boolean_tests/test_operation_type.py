from _martinez import OperationType as Bound

from martinez.boolean import OperationType as Ported


def test_basic():
    assert Bound.__members__ == Ported.__members__
