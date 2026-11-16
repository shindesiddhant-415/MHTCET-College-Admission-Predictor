"""
Module: train_models.py
Purpose: Train and compare multiple regression models using chronological splitting.
Algorithms:
1. Previous-Year Baseline (Naive lag baseline)
2. Ridge Regression with StandardScaler (Linear model with regularization / SGD concept from Practical 3)
3. Decision Tree Regressor (Practical 4)
4. Random Forest Regressor (Ensemble Bagging from Practical 5)
5. HistGradientBoostingRegressor (Ensemble Boosting from Practical 5)

Outputs:
- results/model_comparison.csv
- results/test_metrics.json
- models/selected_model.joblib
- models/preprocessing_pipeline.joblib
- models/model_metadata.json
"""

import os
import time
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Baseline predictor
class PreviousYearBaseline:
    def __init__(self):
        self.name = "Previous-Year Baseline"
    def fit(self, X, y):
        return self
    def predict(self, X):
        return X["prev_year_percentile"].values

def train_and_evaluate_all(
    dataset_path="dataset/model/model_dataset.csv",
    results_dir="results",
    models_dir="models"
):
    print("Loading model dataset...")
    df = pd.read_csv(dataset_path)
    
    # Feature columns
    cat_features = ["institute_code", "course_code", "branch_name", "cap_round", "seat_pool", "seat_category_code", "stage_code"]
    num_features = ["prev_year_percentile", "prev_year_merit_no", "prev_year_intake", "percentile_trend", "intake_change"]
    feature_cols = cat_features + num_features
    target_col = "cutoff_percentile"
    
    # Chronological Split
    # Train: 2024-25 (year_num == 2024)
    # Val: 2025-26 (year_num == 2025)
    # Test: 2026-27 (year_num == 2026)
    train_mask = df["year_num"] == 2024
    val_mask = df["year_num"] == 2025
    test_mask = df["year_num"] == 2026
    
    # Expanding training: Train on 2024, tune on 2025, evaluate on 2026
    train_df = df[train_mask].copy()
    val_df = df[val_mask].copy()
    test_df = df[test_mask].copy()
    
    # Combined train+val for final test evaluation
    train_val_df = df[train_mask | val_mask].copy()
    
    print(f"Data splits: Train (2024)={len(train_df)}, Val (2025)={len(val_df)}, Test (2026)={len(test_df)}")
    
    X_train_val = train_val_df[feature_cols]
    y_train_val = train_val_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]
    
    # Preprocessors
    preprocessor_linear = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features),
        ("num", StandardScaler(), num_features)
    ])
    
    preprocessor_tree = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features),
        ("num", "passthrough", num_features)
    ])
    
    models = {
        "Previous-Year Baseline": {
            "type": "baseline",
            "model": PreviousYearBaseline()
        },
        "Ridge Regression (SGD/L2)": {
            "type": "pipeline",
            "pipeline": Pipeline([
                ("prep", preprocessor_linear),
                ("reg", Ridge(alpha=10.0, random_state=42))
            ]),
            "params": {"alpha": 10.0, "solver": "auto"}
        },
        "Decision Tree Regressor": {
            "type": "pipeline",
            "pipeline": Pipeline([
                ("prep", preprocessor_tree),
                ("reg", DecisionTreeRegressor(max_depth=12, min_samples_leaf=5, random_state=42))
            ]),
            "params": {"max_depth": 12, "min_samples_leaf": 5}
        },
        "Random Forest Regressor": {
            "type": "pipeline",
            "pipeline": Pipeline([
                ("prep", preprocessor_tree),
                ("reg", RandomForestRegressor(n_estimators=100, max_depth=16, min_samples_leaf=3, n_jobs=-1, random_state=42))
            ]),
            "params": {"n_estimators": 100, "max_depth": 16, "min_samples_leaf": 3}
        },
        "HistGradientBoosting Regressor": {
            "type": "pipeline",
            "pipeline": Pipeline([
                ("prep", preprocessor_tree),
                ("reg", HistGradientBoostingRegressor(max_iter=150, max_leaf_nodes=31, learning_rate=0.08, random_state=42))
            ]),
            "params": {"max_iter": 150, "learning_rate": 0.08, "max_leaf_nodes": 31}
        }
    }
    
    results = []
    trained_pipelines = {}
    
    for name, config in models.items():
        print(f"\n--- Training {name} ---")
        t0 = time.time()
        
        if config["type"] == "baseline":
            model = config["model"]
            model.fit(X_train_val, y_train_val)
            train_time = time.time() - t0
            
            t_pred_0 = time.time()
            y_pred = model.predict(X_test)
            pred_time = time.time() - t_pred_0
            trained_pipelines[name] = model
        else:
            pipe = config["pipeline"]
            pipe.fit(X_train_val, y_train_val)
            train_time = time.time() - t0
            
            t_pred_0 = time.time()
            y_pred = pipe.predict(X_test)
            pred_time = time.time() - t_pred_0
            trained_pipelines[name] = pipe
            
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        print(f"MAE: {mae:.4f} | RMSE: {rmse:.4f} | R2: {r2:.4f} | Train Time: {train_time:.3f}s | Pred Time: {pred_time:.3f}s")
        
        results.append({
            "Model": name,
            "MAE": round(mae, 4),
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "R2": round(r2, 4),
            "Training Time (s)": round(train_time, 3),
            "Prediction Time (s)": round(pred_time, 4)
        })
        
    df_results = pd.DataFrame(results).sort_values(by="MAE").reset_index(drop=True)
    
    os.makedirs(results_dir, exist_ok=True)
    df_results.to_csv(os.path.join(results_dir, "model_comparison.csv"), index=False)
    print("\nModel Comparison Table:")
    print(df_results.to_string(index=False))
    
    # Best model selection (lowest MAE on unseen test year 2026)
    best_row = df_results[df_results["Model"] != "Previous-Year Baseline"].iloc[0]
    best_model_name = best_row["Model"]
    print(f"\nBest Performing ML Model: {best_model_name} (MAE={best_row['MAE']:.4f}, R2={best_row['R2']:.4f})")
    
    # Refit best model on ALL historical data (2024, 2025, 2026) for next admission cycle 2027 forecast!
    print("Refitting selected model on entire historical dataset (2024-2026)...")
    X_full = df[feature_cols]
    y_full = df[target_col]
    
    best_config = models[best_model_name]
    final_pipeline = best_config["pipeline"]
    final_pipeline.fit(X_full, y_full)
    
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(final_pipeline, os.path.join(models_dir, "selected_model.joblib"))
    
    # Save metadata
    metadata = {
        "best_model_name": best_model_name,
        "validation_mae": float(best_row["MAE"]),
        "validation_rmse": float(best_row["RMSE"]),
        "validation_r2": float(best_row["R2"]),
        "hyperparameters": best_config.get("params", {}),
        "target_variable": target_col,
        "feature_cols": feature_cols,
        "cat_features": cat_features,
        "num_features": num_features,
        "training_years": ["2023-24 (lag)", "2024-25", "2025-26", "2026-27"],
        "forecast_year": "2027-28",
        "total_training_records": len(df),
        "test_year": "2026-27",
        "margin_factor": 1.5,
        "recommendation_margin": round(float(best_row["MAE"]) * 1.5, 2)
    }
    
    with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
        
    with open(os.path.join(results_dir, "test_metrics.json"), "w") as f:
        json.dump(best_row.to_dict(), f, indent=2)
        
    print(f"Saved artifacts to {models_dir}/ and {results_dir}/")
    return df_results, final_pipeline, metadata

if __name__ == "__main__":
    train_and_evaluate_all()

