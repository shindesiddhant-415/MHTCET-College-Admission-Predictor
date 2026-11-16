"""
Deployment and Model Validation Tests: TC-1 to TC-4
"""

import pytest
import os
import joblib
from src.models.predict_cutoff import predict_single_cutoff
from src.recommendations.recommendation_engine import MHTCETRecommender

@pytest.fixture
def recommender():
    return MHTCETRecommender()

def test_tc1_valid_prediction():
    """TC-1: Valid prediction input returns consistent predicted cutoff between 0 and 100"""
    res = predict_single_cutoff(
        institute_code="06006",
        course_code="0600624510",
        branch_name="Computer Engineering",
        cap_round=1,
        seat_pool="State Level",
        seat_category_code="GOPENS"
    )
    assert res["status"] == "success"
    assert 0.0 <= res["predicted_cutoff"] <= 100.0
    assert abs(res["predicted_cutoff"] - res["previous_year_cutoff"]) < 5.0

def test_tc2_invalid_percentile_rejection(recommender):
    """TC-2: Negative percentile or percentile > 100 must be rejected with ValueError"""
    with pytest.raises(ValueError):
        recommender.recommend(student_percentile=-5.0, seat_category="GOPENS")
        
    with pytest.raises(ValueError):
        recommender.recommend(student_percentile=105.0, seat_category="GOPENS")

def test_tc3_unseen_or_invalid_category(recommender):
    """TC-3: Selected category with no comparable historical record returns clean error status"""
    res = recommender.recommend(student_percentile=95.0, seat_category="NON_EXISTENT_CATEGORY")
    assert res["status"] == "error"
    assert "not recognized" in res["message"]

def test_tc4_new_institute_or_branch():
    """TC-4: New institute or course without historical records returns insufficient data"""
    res = predict_single_cutoff(
        institute_code="99999",
        course_code="9999999999",
        branch_name="Futuristic Engineering",
        cap_round=1,
        seat_pool="State Level",
        seat_category_code="GOPENS"
    )
    assert res["status"] == "insufficient_data"

