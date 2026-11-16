"""
Module: build_features.py
Purpose: Engineer historical lag features, trend metrics, and capacity features
for machine learning modeling without target leakage.
Target dataset: dataset/model/model_dataset.csv
"""

import os
import pandas as pd
import numpy as np

def build_model_dataset(
    cutoffs_path="dataset/processed/cutoffs_long.csv",
    seat_matrix_path="dataset/processed/seat_matrix.csv",
    output_path="dataset/model/model_dataset.csv"
):
    print("Building model dataset with chronological lag features...")
    df_cut = pd.read_csv(cutoffs_path)
    df_sm = pd.read_csv(seat_matrix_path)
    
    # Merge intake information from seat matrix
    df_sm_sub = df_sm[["academic_year", "course_code", "total_intake", "state_seats"]].drop_duplicates()
    df_cut = pd.merge(df_cut, df_sm_sub, on=["academic_year", "course_code"], how="left")
    
    # Primary key for matching combinations across years
    match_cols = ["institute_code", "course_code", "branch_name", "cap_round", "seat_pool", "seat_category_code", "stage_code"]
    
    # Sort chronologically
    df_cut = df_cut.sort_values(by=match_cols + ["year_num"]).reset_index(drop=True)
    
    # Group by combination to calculate lag features
    # Previous year (t-1)
    df_cut["prev_year_percentile"] = df_cut.groupby(match_cols)["cutoff_percentile"].shift(1)
    df_cut["prev_year_merit_no"] = df_cut.groupby(match_cols)["merit_no"].shift(1)
    df_cut["prev_year_intake"] = df_cut.groupby(match_cols)["total_intake"].shift(1)
    
    # Two years earlier (t-2)
    df_cut["prev2_year_percentile"] = df_cut.groupby(match_cols)["cutoff_percentile"].shift(2)
    df_cut["prev2_year_intake"] = df_cut.groupby(match_cols)["total_intake"].shift(2)
    
    # Engineered features
    # Trend: change between previous two years
    df_cut["percentile_trend"] = df_cut["prev_year_percentile"] - df_cut["prev2_year_percentile"]
    # If prev2 is NaN, trend is 0.0
    df_cut["percentile_trend"] = df_cut["percentile_trend"].fillna(0.0)
    
    # Intake change
    df_cut["intake_change"] = df_cut["prev_year_intake"] - df_cut["prev2_year_intake"]
    df_cut["intake_change"] = df_cut["intake_change"].fillna(0.0)
    
    # For rows where prev_year_intake is null, fill from current total_intake
    df_cut["prev_year_intake"] = df_cut["prev_year_intake"].fillna(df_cut["total_intake"])
    
    # We drop rows from the very first year (2023) as targets because they have NO previous-year history (2023 is used purely as historical input)
    model_df = df_cut[df_cut["prev_year_percentile"].notnull()].copy()
    
    # Verify no invalid target percentiles
    model_df = model_df[(model_df["cutoff_percentile"] >= 0) & (model_df["cutoff_percentile"] <= 100)]
    
    # Check shape and summary
    print(f"Total historical target records ready for ML: {len(model_df)}")
    print(f"Year distribution of targets:\n{model_df['academic_year'].value_counts().sort_index()}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    model_df.to_csv(output_path, index=False)
    print(f"Model dataset successfully saved to {output_path}")
    return model_df

if __name__ == "__main__":
    build_model_dataset()
