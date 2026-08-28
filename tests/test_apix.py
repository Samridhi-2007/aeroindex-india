from intelligence.index_engine.apix import price_relative


def test_price_relative_handles_zero_base():
    assert price_relative(0, 100) == 0