"""
Recommendation Engine Tests: TC-5, Suitability Grouping and Ordering
"""

import pytest
from src.recommendations.recommendation_engine import MHTCETRecommender

@pytest.fixture
def recommender():
    return MHTCETRecommender()

def test_tc5_no_matching_preferences(recommender):
    """TC-5: Selected filters returning zero colleges display clear no-results message"""
    res = recommender.recommend(
        student_percentile=90.0,
        seat_category="GOPENS",
        preferred_branches=["Nonexistent Bioengineering"],
        preferred_regions=["Nonexistent City"]
    )
    assert res["status"] == "no_results"
    assert len(res["recommendations"]) == 0

def test_suitability_grouping(recommender):
    """Verify that recommendations contain Safer, Moderate, and/or Reach based on gap"""
    res = recommender.recommend(
        student_percentile=95.0,
        seat_category="GOPENS",
        preferred_branches=["Computer Engineering", "Information Technology"],
        top_n=20
    )
    assert res["status"] == "success"
    recs = res["recommendations"]
    assert len(recs) > 0
    
    for r in recs:
        assert r["suitability_group"] in ["Safer", "Moderate", "Reach"]
        # If Safer, gap should be > margin
        if r["suitability_group"] == "Safer":
            assert r["percentile_gap"] > res["margin"]
        elif r["suitability_group"] == "Moderate":
            assert -res["margin"] <= r["percentile_gap"] <= res["margin"]
        elif r["suitability_group"] == "Reach":
            assert r["percentile_gap"] < -res["margin"]

def test_recommendation_sorting(recommender):
    """Verify Safer options come first, followed by Moderate, followed by Reach"""
    res = recommender.recommend(
        student_percentile=92.0,
        seat_category="GOPENS",
        top_n=20
    )
    recs = res["recommendations"]
    groups = [r["suitability_group"] for r in recs]
    # Check that 'Reach' does not appear before 'Safer'
    if "Safer" in groups and "Reach" in groups:
        first_reach_idx = groups.index("Reach")
        last_safer_idx = max(i for i, g in enumerate(groups) if g == "Safer")
        assert last_safer_idx < first_reach_idx

