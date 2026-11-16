"""
Unit Tests for Data Validation & Preprocessing Pipeline
"""

import os
import pytest
import pandas as pd

def test_cutoff_dataset_exists():
    path = "dataset/processed/cutoffs_long.csv"
    assert os.path.exists(path), f"File {path} does not exist"
    df = pd.read_csv(path)
    assert len(df) > 0, "Cutoff dataset is empty"

def test_seat_matrix_dataset_exists():
    path = "dataset/processed/seat_matrix.csv"
    assert os.path.exists(path), f"File {path} does not exist"
    df = pd.read_csv(path)
    assert len(df) > 0, "Seat matrix dataset is empty"

def test_percentile_ranges():
    df = pd.read_csv("dataset/processed/cutoffs_long.csv")
    assert (df["cutoff_percentile"] >= 0.0).all(), "Found cutoffs < 0.0"
    assert (df["cutoff_percentile"] <= 100.0).all(), "Found cutoffs > 100.0"

def test_merit_number_validity():
    df = pd.read_csv("dataset/processed/cutoffs_long.csv")
    assert (df["merit_no"] > 0).all(), "Found non-positive merit number"

def test_no_critical_nulls():
    df = pd.read_csv("dataset/processed/cutoffs_long.csv")
    critical_cols = ["academic_year", "course_code", "institute_code", "cap_round", "seat_category_code", "cutoff_percentile"]
    for col in critical_cols:
        assert df[col].isnull().sum() == 0, f"Found nulls in critical column {col}"

def test_model_dataset_lags_and_no_leakage():
    path = "dataset/model/model_dataset.csv"
    assert os.path.exists(path), f"File {path} does not exist"
    df = pd.read_csv(path)
    # Target years must be 2024, 2025, 2026
    assert set(df["year_num"].unique()) == {2024, 2025, 2026}
    # Check that prev_year_percentile has no nulls
    assert df["prev_year_percentile"].isnull().sum() == 0

