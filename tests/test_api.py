"""
Unit Tests for FastAPI REST Backend (Powering the React Frontend)
"""

import pytest
from api.main import (
    health_check,
    get_overview,
    get_filter_options,
    get_recommendations,
    get_trends,
    get_model_performance,
    compare_colleges,
    get_manifest,
    RecommendationRequest
)

def test_api_health():
    res = health_check()
    assert res["status"] == "ok"
    assert "React" in res["app"]

def test_api_overview():
    res = get_overview()
    assert res["total_records"] == 32144
    assert res["total_colleges"] == 22
    assert res["validation_mae"] < 0.20
    assert "year_distribution" in res

def test_api_filters():
    res = get_filter_options()
    assert "categories" in res
    assert "GOPENS" in res["categories"]
    assert "pools" in res
    assert "branches" in res
    assert len(res["colleges"]) >= 20

def test_api_recommend_endpoint():
    req = RecommendationRequest(
        student_percentile=92.50,
        seat_category="GOPENS",
        seat_pool="State Level",
        preferred_branches=["Computer Engineering", "Information Technology"],
        cap_round=1,
        top_n=10
    )
    res = get_recommendations(req)
    assert res["status"] == "success"
    assert len(res["recommendations"]) > 0
    assert res["recommendations"][0]["suitability_group"] in ["Safer", "Moderate", "Reach"]

def test_api_trends_endpoint():
    res = get_trends(
        institutes=["COEP Technological University, Pune"],
        branches=["Computer Engineering"],
        category="GOPENS"
    )
    assert "yearly_trends" in res
    assert "round_progression" in res

def test_api_model_performance():
    res = get_model_performance()
    assert "leaderboard" in res
    assert len(res["leaderboard"]) == 5
    assert "plots" in res

def test_api_compare():
    res = compare_colleges(
        institutes=["COEP Technological University, Pune", "Veermata Jijabai Technological Institute (VJTI), Mumbai"],
        branch="Computer Engineering",
        category="GOPENS"
    )
    assert "cutoffs" in res
    assert "intake" in res

