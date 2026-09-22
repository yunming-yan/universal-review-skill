from validator import duplicate

def test_regular():
    assert duplicate(2)
    assert not duplicate(31)
