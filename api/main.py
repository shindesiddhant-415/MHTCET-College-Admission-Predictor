"""
FastAPI Backend for AI-Based MHT-CET Admission Prediction and Personalized Recommendation System.
Provides RESTful endpoints for the React frontend.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.recommendations.recommendation_engine import MHTCETRecommender

# Initialize FastAPI application
app = FastAPI(
    title="MHT-CET Admission Prediction & Recommendation API",
    description="Machine Learning REST API powering the React frontend for Maharashtra Engineering Admissions.",
    version="2.0.0"
)

# Enable CORS for local React development (e.g. Vite default port 5173, 3000, 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommender instance
recommender = MHTCETRecommender()

# Mount results directory to serve diagnostic plots
if os.path.exists("results"):
    app.mount("/results", StaticFiles(directory="results"), name="results")

# Request / Response Schemas
class RecommendationRequest(BaseModel):
    student_percentile: float = Field(..., ge=0.0, le=100.0, description="MHT-CET PCM percentile")
    seat_category: str = Field(..., description="Official seat category code (e.g., GOPENS, GOBCS, TFWS)")
    seat_pool: str = Field(default="State Level", description="Seat pool (State Level, Home University, etc.)")
    preferred_branches: Optional[List[str]] = Field(default=None, description="List of preferred branch names")
    preferred_regions: Optional[List[str]] = Field(default=None, description="List of preferred regions/cities")
    cap_round: int = Field(default=1, ge=1, le=4, description="Target CAP admission round")
    top_n: int = Field(default=20, ge=5, le=100, description="Maximum shortlisted options")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "MHT-CET React+FastAPI Prediction Service"}

@app.get("/api/overview")
def get_overview():
    """Return high-level dataset and model KPI statistics for the dashboard."""
    df_cut = pd.read_csv("dataset/processed/cutoffs_long.csv")
    with open("models/model_metadata.json", "r") as f:
        meta = json.load(f)
        
    year_counts = df_cut["academic_year"].value_counts().to_dict()
    branch_counts = df_cut["branch_name"].value_counts().to_dict()
    
    return {
        "total_records": len(df_cut),
        "total_colleges": df_cut["institute_code"].nunique(),
        "total_branches": df_cut["branch_name"].nunique(),
        "total_categories": df_cut["seat_category_code"].nunique(),
        "best_model_name": meta["best_model_name"],
        "validation_mae": meta["validation_mae"],
        "validation_rmse": meta["validation_rmse"],
        "validation_r2": meta["validation_r2"],
        "forecast_year": meta["forecast_year"],
        "recommendation_margin": meta["recommendation_margin"],
        "year_distribution": year_counts,
        "branch_distribution": branch_counts
    }

@app.get("/api/filters")
def get_filter_options():
    """Return list of supported categories, pools, branches, regions, and colleges."""
    return {
        "categories": recommender.get_supported_categories(),
        "pools": recommender.get_supported_pools(),
        "branches": recommender.get_supported_branches(),
        "regions": recommender.get_supported_regions(),
        "colleges": recommender.get_supported_colleges()
    }

@app.post("/api/recommend")
def get_recommendations(req: RecommendationRequest):
    """Generate personalized college options categorized into Safer, Moderate, Reach."""
    try:
        results = recommender.recommend(
            student_percentile=req.student_percentile,
            seat_category=req.seat_category,
            seat_pool=req.seat_pool,
            preferred_branches=req.preferred_branches,
            preferred_regions=req.preferred_regions,
            cap_round=req.cap_round,
            top_n=req.top_n
        )
        return results
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal prediction error: {str(e)}")

@app.get("/api/trends")
def get_trends(
    institutes: Optional[List[str]] = Query(default=None),
    branches: Optional[List[str]] = Query(default=None),
    category: str = "GOPENS"
):
    """Return historical cutoff trends across academic years and CAP rounds."""
    df = pd.read_csv("dataset/processed/cutoffs_long.csv")
    
    # Filter by category
    sub = df[df["seat_category_code"] == category]
    
    if institutes:
        sub = sub[sub["institute_name"].isin(institutes)]
    if branches:
        sub = sub[sub["branch_name"].isin(branches)]
        
    # Multi-year round 1 trends
    round1 = sub[sub["cap_round"] == 1]
    yearly = round1.groupby(["academic_year", "institute_name", "branch_name"])["cutoff_percentile"].mean().reset_index()
    
    # Round-wise progression (average drop)
    round_drop = sub.groupby(["cap_round", "institute_name"])["cutoff_percentile"].mean().reset_index()
    
    return {
        "yearly_trends": yearly.to_dict(orient="records"),
        "round_progression": round_drop.to_dict(orient="records")
    }

@app.get("/api/model-performance")
def get_model_performance():
    """Return benchmarking leaderboard and diagnostic metadata."""
    df_comp = pd.read_csv("results/model_comparison.csv")
    with open("models/model_metadata.json", "r") as f:
        meta = json.load(f)
        
    return {
        "leaderboard": df_comp.to_dict(orient="records"),
        "metadata": meta,
        "plots": {
            "actual_vs_predicted": "/results/actual_vs_predicted.png",
            "error_distribution": "/results/error_distribution.png",
            "model_comparison_bar": "/results/model_comparison_bar.png",
            "feature_importance": "/results/feature_importance.png",
            "eda_cutoff_distribution": "/results/eda_cutoff_distribution.png",
            "eda_branch_boxplot": "/results/eda_branch_boxplot.png",
            "eda_year_trend": "/results/eda_year_trend.png"
        }
    }

@app.get("/api/compare")
def compare_colleges(
    institutes: List[str] = Query(...),
    branch: str = Query(...),
    category: str = Query("GOPENS")
):
    """Side-by-side cutoff comparison and sanctioned intake breakdown."""
    df_cut = pd.read_csv("dataset/processed/cutoffs_long.csv")
    df_sm = pd.read_csv("dataset/processed/seat_matrix.csv")
    
    cut_sub = df_cut[
        (df_cut["institute_name"].isin(institutes)) &
        (df_cut["branch_name"] == branch) &
        (df_cut["seat_category_code"] == category) &
        (df_cut["cap_round"] == 1)
    ]
    
    sm_sub = df_sm[
        (df_sm["institute_name"].isin(institutes)) &
        (df_sm["branch_name"] == branch) &
        (df_sm["academic_year"] == "2026-27")
    ]
    
    return {
        "cutoffs": cut_sub[["academic_year", "institute_name", "cutoff_percentile"]].to_dict(orient="records"),
        "intake": sm_sub[[
            "institute_name", "total_intake", "state_seats",
            "minority_seats", "all_india_seats", "institute_seats"
        ]].to_dict(orient="records")
    }

@app.get("/api/manifest")
def get_manifest():
    """Return source documents manifest and data quality report."""
    manifest = pd.read_csv("docs/source_manifest.csv")
    quality = pd.read_csv("dataset/processed/data_quality_report.csv")
    return {
        "manifest": manifest.to_dict(orient="records"),
        "quality_report": quality.to_dict(orient="records")
    }

# Mount React production build if available
dist_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(dist_dir):
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)

