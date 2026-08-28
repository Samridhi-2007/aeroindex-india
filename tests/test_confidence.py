from intelligence.models import Weights
from intelligence.quality.confidence import calculate_confidence
from tests.test_core import obs


def test_confidence_is_bounded():
    result = calculate_confidence([obs()], Weights({"R": 1}, {1: 1}))
    assert 0 <= result["overall_confidence"] <= 100