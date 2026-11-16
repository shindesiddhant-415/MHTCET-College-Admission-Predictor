"""
Module: recommendation_engine.py
Purpose: Personalized engineering college recommendation engine using ML predicted cutoffs,
transparent percentile gap calculation, and Safer / Moderate / Reach suitability grouping.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np

# Mapping of institute codes to regions/cities
INSTITUTE_REGIONS = {
    "06006": "Pune",
    "03012": "Mumbai",
    "06271": "Pune",
    "03014": "Mumbai",
    "06273": "Pune",
    "06284": "Pune",
    "06007": "Sangli",
    "01002": "Amravati",
    "02008": "Chhatrapati Sambhajinagar",
    "06004": "Satara",
    "04003": "Chandrapur",
    "02018": "Nanded",
    "03199": "Mumbai",
    "03198": "Mumbai",
    "06288": "Pune",
    "06277": "Pune",
    "06274": "Pune",
    "06278": "Pune",
    "04115": "Nagpur",
    "05121": "Nashik",
    "06275": "Pune",
    "03182": "Mumbai"
}

class MHTCETRecommender:
    def __init__(
        self,
        model_path="models/selected_model.joblib",
        metadata_path="models/model_metadata.json",
        cutoffs_path="dataset/processed/cutoffs_long.csv",
        seat_matrix_path="dataset/processed/seat_matrix.csv"
    ):
        self.model = joblib.load(model_path)
        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)
            
        self.margin = self.metadata.get("recommendation_margin", 0.20)
        self.df_cut = pd.read_csv(cutoffs_path)
        self.df_sm = pd.read_csv(seat_matrix_path)
        
        # Add region
        self.df_cut["region"] = self.df_cut["institute_code"].astype(str).str.zfill(5).map(INSTITUTE_REGIONS).fillna("Maharashtra")
        
        # Prepare lookup dictionary for latest year (2026-27) to form lag features for 2027 prediction
        self.latest_year_cutoffs = self.df_cut[self.df_cut["academic_year"] == "2026-27"].copy()
        self.prev_year_cutoffs = self.df_cut[self.df_cut["academic_year"] == "2025-26"].copy()
        
    def get_supported_categories(self):
        return sorted(self.df_cut["seat_category_code"].unique().tolist())
        
    def get_supported_pools(self):
        return sorted(self.df_cut["seat_pool"].unique().tolist())
        
    def get_supported_branches(self):
        return sorted(self.df_cut["branch_name"].unique().tolist())
        
    def get_supported_regions(self):
        return sorted(list(set(INSTITUTE_REGIONS.values())))
        
    def get_supported_colleges(self):
        df_colleges = self.df_cut[["institute_code", "institute_name", "region"]].drop_duplicates()
        return df_colleges.to_dict(orient="records")

    def recommend(
        self,
        student_percentile: float,
        seat_category: str,
        seat_pool: str = "State Level",
        preferred_branches: list = None,
        preferred_regions: list = None,
        cap_round: int = 1,
        top_n: int = 20
    ):
        """
        Generate personalized college recommendations grouped into Safer, Moderate, Reach.
        """
        # Input validation
        if not (0.0 <= student_percentile <= 100.0):
            raise ValueError(f"Student percentile {student_percentile} must be between 0.0 and 100.0")
            
        if seat_category not in self.get_supported_categories():
            return {
                "status": "error",
                "message": f"Selected seat category '{seat_category}' is not recognized in historical official CAP records.",
                "recommendations": []
            }
            
        # Filter available options for the selected round, category, and pool
        pool_filter = self.latest_year_cutoffs[
            (self.latest_year_cutoffs["cap_round"] == cap_round) &
            (self.latest_year_cutoffs["seat_category_code"] == seat_category)
        ].copy()
        
        # If pool matches or fallback to available
        if seat_pool:
            pool_matching = pool_filter[pool_filter["seat_pool"] == seat_pool]
            if len(pool_matching) > 0:
                pool_filter = pool_matching
                
        if preferred_branches:
            pool_filter = pool_filter[pool_filter["branch_name"].isin(preferred_branches)]
            
        if preferred_regions:
            pool_filter = pool_filter[pool_filter["region"].isin(preferred_regions)]
            
        if pool_filter.empty:
            return {
                "status": "no_results",
                "message": "No college options match the selected filters. Please broaden your branch, region, or pool preferences.",
                "recommendations": []
            }
            
        # Build feature rows for 2027 prediction using 2026 and 2025 data as lags
        candidate_rows = []
        for _, row in pool_filter.iterrows():
            c_code = row["course_code"]
            inst_code = row["institute_code"]
            b_name = row["branch_name"]
            st_code = row["stage_code"]
            
            # Lag 1: 2026 cutoff
            prev_pct = row["cutoff_percentile"]
            prev_merit = row["merit_no"]
            
            # Lag 2: 2025 cutoff
            prev2_match = self.prev_year_cutoffs[
                (self.prev_year_cutoffs["course_code"] == c_code) &
                (self.prev_year_cutoffs["cap_round"] == cap_round) &
                (self.prev_year_cutoffs["seat_category_code"] == seat_category) &
                (self.prev_year_cutoffs["stage_code"] == st_code)
            ]
            
            if not prev2_match.empty:
                prev2_pct = prev2_match.iloc[0]["cutoff_percentile"]
                trend = prev_pct - prev2_pct
            else:
                trend = 0.0
                
            intake = 120  # default
            sm_match = self.df_sm[
                (self.df_sm["course_code"] == c_code) &
                (self.df_sm["academic_year"] == "2026-27")
            ]
            if not sm_match.empty:
                intake = sm_match.iloc[0]["total_intake"]
                
            candidate_rows.append({
                "institute_code": str(inst_code).zfill(5),
                "institute_name": row["institute_name"],
                "region": row["region"],
                "course_code": str(c_code),
                "branch_name": b_name,
                "cap_round": cap_round,
                "seat_pool": row["seat_pool"],
                "seat_category_code": seat_category,
                "stage_code": st_code,
                "prev_year_percentile": prev_pct,
                "prev_year_merit_no": prev_merit,
                "prev_year_intake": intake,
                "percentile_trend": trend,
                "intake_change": 0.0,
                "history_2026": prev_pct,
                "history_2025": prev2_match.iloc[0]["cutoff_percentile"] if not prev2_match.empty else None
            })
            
        df_candidates = pd.DataFrame(candidate_rows)
        feature_cols = [
            "institute_code", "course_code", "branch_name", "cap_round",
            "seat_pool", "seat_category_code", "stage_code",
            "prev_year_percentile", "prev_year_merit_no", "prev_year_intake",
            "percentile_trend", "intake_change"
        ]
        
        # Model Inference
        predicted_cutoffs = self.model.predict(df_candidates[feature_cols])
        df_candidates["predicted_cutoff"] = np.round(predicted_cutoffs, 2)
        df_candidates["student_percentile"] = round(student_percentile, 2)
        
        # Calculate Percentile Gap
        # Gap = Student Percentile - Predicted Cutoff
        # Positive gap: student score is above predicted cutoff
        # Negative gap: student score is below predicted cutoff
        df_candidates["percentile_gap"] = np.round(df_candidates["student_percentile"] - df_candidates["predicted_cutoff"], 2)
        
        # Suitability Grouping
        # Margin M = 1.5 * MAE (~0.17 - 0.20 percentile points)
        # Safer: Gap > M
        # Moderate: -M <= Gap <= M
        # Reach: Gap < -M
        def assign_group(gap):
            if gap > self.margin:
                return "Safer"
            elif gap >= -self.margin:
                return "Moderate"
            else:
                return "Reach"
                
        def explain_recommendation(row):
            gap = row["percentile_gap"]
            group = row["suitability_group"]
            cutoff = row["predicted_cutoff"]
            if group == "Safer":
                return f"Student percentile ({student_percentile:.2f}) is +{gap:.2f} above estimated cutoff ({cutoff:.2f}). Safe choice within admission probability window."
            elif group == "Moderate":
                return f"Student percentile ({student_percentile:.2f}) is within {abs(gap):.2f} pts of estimated cutoff ({cutoff:.2f}). Highly competitive match."
            else:
                return f"Student percentile ({student_percentile:.2f}) is {abs(gap):.2f} pts below estimated cutoff ({cutoff:.2f}). Ambitious/Dream option."

        df_candidates["suitability_group"] = df_candidates["percentile_gap"].apply(assign_group)
        df_candidates["explanation"] = df_candidates.apply(explain_recommendation, axis=1)
        
        # Sort recommendations:
        # Group order: Safer first (sorted by closest to margin), then Moderate, then Reach
        group_priority = {"Safer": 1, "Moderate": 2, "Reach": 3}
        df_candidates["group_priority"] = df_candidates["suitability_group"].map(group_priority)
        
        # Within Safer, prioritize choices that are competitive (gap between 0 and 5)
        # Order by predicted cutoff descending
        df_sorted = df_candidates.sort_values(
            by=["group_priority", "predicted_cutoff"],
            ascending=[True, False]
        ).reset_index(drop=True)
        
        final_recs = df_sorted.head(top_n).copy()
        
        return {
            "status": "success",
            "student_percentile": student_percentile,
            "seat_category": seat_category,
            "seat_pool": seat_pool,
            "cap_round": cap_round,
            "margin": self.margin,
            "total_matches": len(df_candidates),
            "recommendations": final_recs.to_dict(orient="records")
        }

if __name__ == "__main__":
    recommender = MHTCETRecommender()
    print("Testing recommendation engine for student with 92.50 percentile, GOPENS, Pune & Mumbai:")
    results = recommender.recommend(
        student_percentile=92.50,
        seat_category="GOPENS",
        seat_pool="State Level",
        preferred_branches=["Computer Engineering", "Information Technology", "Artificial Intelligence and Data Science"],
        top_n=10
    )
    print(f"Status: {results['status']}, Total matches: {results['total_matches']}")
    for r in results["recommendations"][:5]:
        print(f"[{r['suitability_group']}] {r['institute_name']} | {r['branch_name']} | Cutoff: {r['predicted_cutoff']} | Gap: {r['percentile_gap']:+.2f}")
