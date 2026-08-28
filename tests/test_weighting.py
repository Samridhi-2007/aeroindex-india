from intelligence.index_engine.weighting import representative_fares
from tests.test_core import obs


def test_representative_fare_is_median():
    assert representative_fares([obs(fare=1), obs(fare=3, observation_id="2"), obs(fare=2, observation_id="3")])[("R", 1, "base")] == 2