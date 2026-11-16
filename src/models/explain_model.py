"""
Module: explain_model.py
Purpose: Generate critical evaluation plots: Actual vs Predicted, Residual distributions,
Feature importance, and error breakdowns by round and branch.
"""

import os
os.environ['MPLCONFIGDIR'] = os.path.abspath("results/.matplotlib_cache")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import joblib

def generate_evaluation_visualizations(
    model_path="models/selected_model.joblib",
    dataset_path="dataset/model/model_dataset.csv",
    results_dir="results"
):
    print("Generating comprehensive model evaluation plots...")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs("report/screenshots", exist_ok=True)
    
    df = pd.read_csv(dataset_path)
    test_df = df[df["year_num"] == 2026].copy()
    
    pipeline = joblib.load(model_path)
    feature_cols = [
        "institute_code", "course_code", "branch_name", "cap_round",
        "seat_pool", "seat_category_code", "stage_code",
        "prev_year_percentile", "prev_year_merit_no", "prev_year_intake",
        "percentile_trend", "intake_change"
    ]
    
    y_test = test_df["cutoff_percentile"].values
    y_pred = pipeline.predict(test_df[feature_cols])
    residuals = y_test - y_pred
    test_df["predicted"] = y_pred
    test_df["residual"] = residuals
    test_df["abs_error"] = np.abs(residuals)
    
    sns.set_theme(style="whitegrid")
    
    # 1. Actual vs Predicted
    plt.figure(figsize=(7, 6))
    plt.scatter(y_test, y_pred, alpha=0.3, color="#1f77b4", edgecolors='none', s=20)
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], color="#e74c3c", linestyle="--", linewidth=2, label="Ideal 45° Line (y=x)")
    plt.title("Actual vs Predicted Cutoff Percentile (Test Year 2026-27)", fontsize=12, fontweight='bold')
    plt.xlabel("Actual Cutoff Percentile", fontsize=10)
    plt.ylabel("Predicted Cutoff Percentile", fontsize=10)
    plt.legend()
    plt.tight_layout()
    p1 = os.path.join(results_dir, "actual_vs_predicted.png")
    plt.savefig(p1, dpi=200)
    plt.savefig("report/screenshots/actual_vs_predicted.png", dpi=200)
    plt.close()
    
    # 2. Residual Distribution
    plt.figure(figsize=(7, 5))
    sns.histplot(residuals, kde=True, bins=40, color="#2ecc71", edgecolor="black")
    plt.axvline(0, color="#e74c3c", linestyle="--", linewidth=1.5, label="Zero Error")
    plt.axvline(np.mean(residuals), color="#2980b9", linestyle=":", linewidth=1.5, label=f"Mean Error: {np.mean(residuals):.3f}")
    plt.title("Prediction Residuals Distribution (Actual - Predicted)", fontsize=12, fontweight='bold')
    plt.xlabel("Residual (Percentile points)", fontsize=10)
    plt.ylabel("Frequency", fontsize=10)
    plt.legend()
    plt.tight_layout()
    p2 = os.path.join(results_dir, "error_distribution.png")
    plt.savefig(p2, dpi=200)
    plt.savefig("report/screenshots/error_distribution.png", dpi=200)
    plt.close()
    
    # 3. Model Comparison Bar Chart
    df_comp = pd.read_csv(os.path.join(results_dir, "model_comparison.csv"))
    plt.figure(figsize=(9, 4.5))
    bars = plt.barh(df_comp["Model"], df_comp["MAE"], color="#3498db")
    plt.xlabel("Mean Absolute Error (MAE in percentile points) ↓", fontsize=10)
    plt.title("Regression Models Comparative Performance (Held-out Test Year 2026)", fontsize=12, fontweight='bold')
    plt.gca().invert_yaxis()
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.003, bar.get_y() + bar.get_height()/2, f"{width:.4f}", va='center', fontsize=9, fontweight='bold')
    plt.xlim(0, max(df_comp["MAE"])*1.2)
    plt.tight_layout()
    p3 = os.path.join(results_dir, "model_comparison_bar.png")
    plt.savefig(p3, dpi=200)
    plt.savefig("report/screenshots/model_comparison_bar.png", dpi=200)
    plt.close()
    
    # 4. MAE by CAP Round
    round_mae = test_df.groupby("cap_round")["abs_error"].mean().reset_index()
    plt.figure(figsize=(6, 4))
    sns.barplot(data=round_mae, x="cap_round", y="abs_error", palette="Blues_d")
    plt.title("Mean Absolute Error by CAP Round", fontsize=12, fontweight='bold')
    plt.xlabel("CAP Admission Round", fontsize=10)
    plt.ylabel("MAE (Percentile points)", fontsize=10)
    plt.tight_layout()
    p4 = os.path.join(results_dir, "cap_round_error.png")
    plt.savefig(p4, dpi=200)
    plt.close()
    
    # 5. MAE by Engineering Branch
    branch_mae = test_df.groupby("branch_name")["abs_error"].mean().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 4.5))
    sns.barplot(data=branch_mae, y="branch_name", x="abs_error", palette="viridis")
    plt.title("Mean Absolute Error by Engineering Branch", fontsize=12, fontweight='bold')
    plt.xlabel("MAE (Percentile points)", fontsize=10)
    plt.ylabel("Branch", fontsize=10)
    plt.tight_layout()
    p5 = os.path.join(results_dir, "branch_error.png")
    plt.savefig(p5, dpi=200)
    plt.close()
    
    # 6. Feature Importance / Linear Coefficients
    regressor = pipeline.named_steps["reg"]
    preprocessor = pipeline.named_steps["prep"]
    try:
        feature_names = preprocessor.get_feature_names_out()
        if hasattr(regressor, "coef_"):
            coefs = regressor.coef_
            df_feat = pd.DataFrame({"feature": feature_names, "importance": np.abs(coefs)})
            df_feat = df_feat.sort_values(by="importance", ascending=False).head(15)
            
            plt.figure(figsize=(8, 5))
            sns.barplot(data=df_feat, y="feature", x="importance", palette="magma")
            plt.title("Top Feature Importances / Coefficients (Ridge)", fontsize=12, fontweight='bold')
            plt.xlabel("Absolute Coefficient Weight", fontsize=10)
            plt.ylabel("Feature", fontsize=10)
            plt.tight_layout()
            p6 = os.path.join(results_dir, "feature_importance.png")
            plt.savefig(p6, dpi=200)
            plt.savefig("report/screenshots/feature_importance.png", dpi=200)
            plt.close()
    except Exception as e:
        print(f"Feature importance plot note: {e}")
        
    print("All evaluation plots generated successfully.")

if __name__ == "__main__":
    generate_evaluation_visualizations()

