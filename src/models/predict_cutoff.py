"""
Module: predict_cutoff.py
Purpose: Estimate next-cycle cutoff percentile for an individual college-branch-category combination.
"""

import sys
import json
import joblib
import pandas as pd
import numpy as np

def predict_single_cutoff(
    institute_code: str,
    course_code: str,
    branch_name: str,
    cap_round: int,
    seat_pool: str,
    seat_category_code: str,
    stage_code: str = "I",
    model_path="models/selected_model.joblib",
    cutoffs_path="dataset/processed/cutoffs_long.csv"
):
    pipeline = joblib.load(model_path)
    df_cut = pd.read_csv(cutoffs_path)
    
    # Locate recent historical records
    hist_2026 = df_cut[
        (df_cut["academic_year"] == "2026-27") &
        (df_cut["course_code"] == int(course_code) if str(course_code).isdigit() else df_cut["course_code"] == course_code) &
        (df_cut["cap_round"] == cap_round) &
        (df_cut["seat_category_code"] == seat_category_code)
    ]
    
    if hist_2026.empty:
        return {
            "status": "insufficient_data",
            "message": "Insufficient historical data available for this specific combination."
        }
        
    prev_pct = hist_2026.iloc[0]["cutoff_percentile"]
    prev_merit = hist_2026.iloc[0]["merit_no"]
    
    hist_2025 = df_cut[
        (df_cut["academic_year"] == "2025-26") &
        (df_cut["course_code"] == int(course_code) if str(course_code).isdigit() else df_cut["course_code"] == course_code) &
        (df_cut["cap_round"] == cap_round) &
        (df_cut["seat_category_code"] == seat_category_code)
    ]
    
    trend = 0.0
    if not hist_2025.empty:
        trend = prev_pct - hist_2025.iloc[0]["cutoff_percentile"]
        
    features = pd.DataFrame([{
        "institute_code": str(institute_code).zfill(5),
        "course_code": str(course_code),
        "branch_name": branch_name,
        "cap_round": cap_round,
        "seat_pool": seat_pool,
        "seat_category_code": seat_category_code,
        "stage_code": stage_code,
        "prev_year_percentile": prev_pct,
        "prev_year_merit_no": prev_merit,
        "prev_year_intake": 120,
        "percentile_trend": trend,
        "intake_change": 0.0
    }])
    
    pred = pipeline.predict(features)[0]
    return {
        "status": "success",
        "predicted_cutoff": round(float(pred), 4),
        "previous_year_cutoff": round(float(prev_pct), 4),
        "historical_trend": round(float(trend), 4),
        "institute_code": institute_code,
        "course_code": course_code,
        "cap_round": cap_round,
        "seat_category_code": seat_category_code
    }

if __name__ == "__main__":
    res = predict_single_cutoff(
        institute_code="06006",
        course_code="0600624510",
        branch_name="Computer Engineering",
        cap_round=1,
        seat_pool="State Level",
        seat_category_code="GOPENS"
    )
    print("Sample Single Prediction Result:")
    print(json.dumps(res, indent=2))
