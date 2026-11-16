"""
Module: generate_eda_plots.py
Purpose: Create essential Exploratory Data Analysis (EDA) visualizations:
1. Cutoff Percentile Distribution
2. Year-wise Cutoff Trend
3. CAP Round Comparison
4. Branch-wise Box Plot
5. Category-wise Distribution
6. Correlation Heatmap
"""

import os
os.environ['MPLCONFIGDIR'] = os.path.abspath("results/.matplotlib_cache")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def generate_all_eda_plots(
    cutoffs_path="dataset/processed/cutoffs_long.csv",
    output_dir="results"
):
    print("Generating EDA visualizations...")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("report/screenshots", exist_ok=True)
    
    df = pd.read_csv(cutoffs_path)
    sns.set_theme(style="whitegrid")
    
    # 1. Cutoff Percentile Distribution
    plt.figure(figsize=(7, 4.5))
    sns.histplot(df["cutoff_percentile"], kde=True, bins=35, color="#16a085")
    plt.title("MHT-CET CAP Cutoff Percentile Distribution (All Years)", fontsize=11, fontweight="bold")
    plt.xlabel("Cutoff Percentile", fontsize=9)
    plt.ylabel("Frequency", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_cutoff_distribution.png"), dpi=200)
    plt.savefig("report/screenshots/eda_cutoff_distribution.png", dpi=200)
    plt.close()
    
    # 2. Year-wise Cutoff Trend
    year_trends = df.groupby(["academic_year", "branch_name"])["cutoff_percentile"].mean().reset_index()
    plt.figure(figsize=(9, 5))
    sns.lineplot(data=year_trends, x="academic_year", y="cutoff_percentile", hue="branch_name", marker="o", linewidth=2)
    plt.title("Branch-wise Mean Cutoff Percentile Movement (2023-24 to 2026-27)", fontsize=11, fontweight="bold")
    plt.xlabel("Academic Year", fontsize=9)
    plt.ylabel("Mean Cutoff Percentile", fontsize=9)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_year_trend.png"), dpi=200)
    plt.savefig("report/screenshots/eda_year_trend.png", dpi=200)
    plt.close()
    
    # 3. CAP Round Comparison
    plt.figure(figsize=(7, 4.5))
    sns.boxplot(data=df, x="cap_round", y="cutoff_percentile", palette="Set2")
    plt.title("Cutoff Percentile Spread Across CAP Rounds", fontsize=11, fontweight="bold")
    plt.xlabel("CAP Round", fontsize=9)
    plt.ylabel("Cutoff Percentile", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_cap_rounds.png"), dpi=200)
    plt.savefig("report/screenshots/eda_cap_rounds.png", dpi=200)
    plt.close()
    
    # 4. Branch-wise Box Plot
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, y="branch_name", x="cutoff_percentile", palette="coolwarm")
    plt.title("Cutoff Percentile Distribution by Engineering Branch", fontsize=11, fontweight="bold")
    plt.xlabel("Cutoff Percentile", fontsize=9)
    plt.ylabel("Branch", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_branch_boxplot.png"), dpi=200)
    plt.savefig("report/screenshots/eda_branch_boxplot.png", dpi=200)
    plt.close()
    
    # 5. Category-wise Distribution
    cat_order = df.groupby("seat_category_code")["cutoff_percentile"].median().sort_values(ascending=False).index
    plt.figure(figsize=(10, 4.5))
    sns.boxplot(data=df, x="seat_category_code", y="cutoff_percentile", order=cat_order, palette="tab20")
    plt.title("Cutoff Distribution by Official Seat Category Code", fontsize=11, fontweight="bold")
    plt.xlabel("Seat Category Code", fontsize=9)
    plt.ylabel("Cutoff Percentile", fontsize=9)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_category_distribution.png"), dpi=200)
    plt.savefig("report/screenshots/eda_category_distribution.png", dpi=200)
    plt.close()
    
    # 6. Correlation Heatmap
    num_cols = ["year_num", "cap_round", "merit_no", "cutoff_percentile"]
    corr = df[num_cols].corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap="Blues", fmt=".3f", cbar=True)
    plt.title("Correlation Matrix of Numerical Features", fontsize=11, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_correlation_heatmap.png"), dpi=200)
    plt.savefig("report/screenshots/eda_correlation_heatmap.png", dpi=200)
    plt.close()
    
    print("EDA plots created successfully.")

if __name__ == "__main__":
    generate_all_eda_plots()

