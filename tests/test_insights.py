from intelligence.insights.explanations import generate_index_movement_insight


def test_index_movement_insight_is_structured():
    assert generate_index_movement_insight(102)["direction"] == "UP"