from intelligence.index_engine.contributions import route_contributions


def test_route_contribution_reconciles():
    result = route_contributions([{"route": "R", "weighted_contribution": 60}], {"R": 1})
    assert result[0]["contribution"] == 60