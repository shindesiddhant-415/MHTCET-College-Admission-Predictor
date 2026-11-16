"""
Module: validate_data.py
Purpose: Perform comprehensive data quality checks and validation on parsed cutoff records
and seat matrices, generating dataset/processed/data_quality_report.csv.
"""

import os
import pandas as pd
import numpy as np

def validate_datasets(
    cutoffs_path="dataset/processed/cutoffs_long.csv",
    seat_matrix_path="dataset/processed/seat_matrix.csv",
    output_report="dataset/processed/data_quality_report.csv"
):
    print("Running comprehensive data validation checks...")
    df_cut = pd.read_csv(cutoffs_path)
    df_sm = pd.read_csv(seat_matrix_path)
    
    total_rows = len(df_cut)
    
    # 1. Source traceability
    has_source_file = df_cut["source_file"].notnull() & (df_cut["source_file"] != "")
    has_source_page = df_cut["source_page"].notnull() & (df_cut["source_page"] > 0)
    traceable_rows = (has_source_file & has_source_page).sum()
    
    # 2. Percentile validity (0 <= percentile <= 100)
    valid_pct = (df_cut["cutoff_percentile"] >= 0.0) & (df_cut["cutoff_percentile"] <= 100.0)
    invalid_pct_count = (~valid_pct).sum()
    missing_pct_count = df_cut["cutoff_percentile"].isnull().sum()
    
    # 3. Merit number validity
    valid_merit = (df_cut["merit_no"] > 0) & df_cut["merit_no"].notnull()
    invalid_merit_count = (~valid_merit).sum()
    
    # 4. Duplicate detection
    key_cols = ["academic_year", "cap_round", "course_code", "seat_pool", "seat_category_code", "stage_code"]
    duplicate_count = df_cut.duplicated(subset=key_cols).sum()
    
    # 5. Unmatched institute or course codes
    cut_courses = set(df_cut["course_code"].unique())
    sm_courses = set(df_sm["course_code"].unique())
    unmatched_courses = len(cut_courses - sm_courses)
    
    # 6. Overall validity
    valid_rows_count = total_rows - (invalid_pct_count + missing_pct_count + duplicate_count)
    
    report_data = [
        {"metric": "total_extracted_rows", "value": total_rows, "status": "INFO"},
        {"metric": "valid_parsed_rows", "value": valid_rows_count, "status": "PASS"},
        {"metric": "rows_with_missing_percentiles", "value": missing_pct_count, "status": "PASS" if missing_pct_count == 0 else "FAIL"},
        {"metric": "rows_with_invalid_values", "value": invalid_pct_count + invalid_merit_count, "status": "PASS" if (invalid_pct_count + invalid_merit_count) == 0 else "FAIL"},
        {"metric": "duplicate_rows", "value": duplicate_count, "status": "PASS" if duplicate_count == 0 else "FAIL"},
        {"metric": "unmatched_institutes_courses", "value": unmatched_courses, "status": "PASS" if unmatched_courses == 0 else "WARN"},
        {"metric": "source_traceable_rows", "value": traceable_rows, "status": "PASS" if traceable_rows == total_rows else "WARN"},
        {"metric": "seat_matrix_total_rows", "value": len(df_sm), "status": "INFO"},
        {"metric": "distinct_institutes", "value": df_cut["institute_code"].nunique(), "status": "INFO"},
        {"metric": "distinct_branches", "value": df_cut["branch_name"].nunique(), "status": "INFO"},
        {"metric": "distinct_categories", "value": df_cut["seat_category_code"].nunique(), "status": "INFO"},
        {"metric": "percentage_verified", "value": 100.0 * (valid_rows_count / total_rows) if total_rows > 0 else 0.0, "status": "PASS"}
    ]
    
    df_report = pd.DataFrame(report_data)
    os.makedirs(os.path.dirname(output_report), exist_ok=True)
    df_report.to_csv(output_report, index=False)
    print("Data quality report generated successfully:")
    print(df_report.to_string(index=False))
    return df_report

if __name__ == "__main__":
    validate_datasets()

