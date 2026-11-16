"""
Generate architecture diagram image for the report and README.
"""

import os
os.environ['MPLCONFIGDIR'] = os.path.abspath("results/.matplotlib_cache")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_architecture_diagram(output_path="results/architecture_diagram.png"):
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=200)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis("off")
    
    # Background styling
    fig.patch.set_facecolor('#ffffff')
    
    # Box styles
    box_blue = dict(boxstyle="round,pad=0.5", fc="#e8f4f8", ec="#0288d1", lw=1.5)
    box_green = dict(boxstyle="round,pad=0.5", fc="#e8f8f5", ec="#26a69a", lw=1.5)
    box_orange = dict(boxstyle="round,pad=0.5", fc="#fef5e7", ec="#f39c12", lw=1.5)
    box_purple = dict(boxstyle="round,pad=0.5", fc="#f4ecf7", ec="#8e44ad", lw=1.5)
    
    # 1. Data Ingestion
    ax.text(1.8, 6.0, "1. Official CET Cell Records\n• 14 CAP Cutoff PDFs (2023-26)\n• 4 Sanctioned Seat Matrices\n• Maharashtra Pool Focus", 
            ha="center", va="center", bbox=box_blue, fontsize=9, fontweight="bold")
    
    # 2. Text Extraction & Parsing
    ax.text(1.8, 3.8, "2. Extraction & Normalization\n• PyMuPDF Page-by-Page Extraction\n• Regex Table Normalizer\n• 32,144 Long-Format Records\n• Data Quality & Audit Report", 
            ha="center", va="center", bbox=box_blue, fontsize=9, fontweight="bold")
    
    # 3. Feature Store
    ax.text(5.5, 6.0, "3. Feature Engineering\n• Prior-Year Lags (t-1, t-2)\n• Cutoff Momentum Trend\n• Capacity & Intake Shift\n• Categorical Encodings (One-Hot)", 
            ha="center", va="center", bbox=box_green, fontsize=9, fontweight="bold")
    
    # 4. Chronological ML Modeling
    ax.text(5.5, 3.8, "4. Chronological ML Models\n• Train 2024 | Val 2025 | Test 2026\n• Previous-Year Cutoff Baseline\n• Ridge Regression (SGD/L2)\n• Decision Tree & Random Forest\n• HistGradientBoosting Regressor", 
            ha="center", va="center", bbox=box_green, fontsize=9, fontweight="bold")
    
    # 5. Recommendation Engine
    ax.text(9.2, 6.0, "5. Recommendation Engine\n• Percentile Gap: Gap = P_student - P_cut\n• Validation MAE Margin (M = 1.5*MAE)\n• Suitability Grouping:\n  - Safer: Gap > M\n  - Moderate: |Gap| <= M\n  - Reach: Gap < -M", 
            ha="center", va="center", bbox=box_orange, fontsize=9, fontweight="bold")
    
    # 6. Streamlit Deployment
    ax.text(9.2, 3.8, "6. Streamlit Web Deployment\n• Interactive Student Profile Form\n• Historical Trends (Plotly)\n• Side-by-Side College Comparison\n• Model Leaderboard & Diagnostics\n• CSV Shortlist Export", 
            ha="center", va="center", bbox=box_purple, fontsize=9, fontweight="bold")
    
    # Bottom Banner: Responsible AI
    box_banner = dict(boxstyle="round,pad=0.6", fc="#fdfefe", ec="#7f8c8d", lw=1.2, ls="--")
    ax.text(5.5, 1.2, "Responsible AI & Educational Impact (SDG 4 & SDG 10)\n• Privacy by Design: Zero personal identifying logs or document uploads required\n• Explainable Decision Support: Transparent error margins, prior cutoff history, and rationale for every tag\n• Fair Quota Handling: Full official category preservation (GOPENS, GOBCS, GSCS, GSTS, EWS, TFWS)",
            ha="center", va="center", bbox=box_banner, fontsize=8.5, color="#2c3e50")
    
    # Draw Arrows
    arrow = dict(arrowstyle="->", lw=2, color="#34495e")
    ax.annotate("", xy=(1.8, 4.7), xytext=(1.8, 5.1), arrowprops=arrow)
    ax.annotate("", xy=(3.8, 3.8), xytext=(3.3, 3.8), arrowprops=arrow)
    ax.annotate("", xy=(5.5, 4.9), xytext=(5.5, 5.2), arrowprops=arrow)
    ax.annotate("", xy=(7.4, 6.0), xytext=(7.1, 6.0), arrowprops=arrow)
    ax.annotate("", xy=(9.2, 4.7), xytext=(9.2, 5.1), arrowprops=arrow)
    ax.annotate("", xy=(5.5, 2.0), xytext=(5.5, 2.8), arrowprops=arrow)
    
    plt.title("End-to-End System Architecture: MHT-CET Admission Predictor & Recommender", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.savefig("report/screenshots/architecture_diagram.png", dpi=200)
    plt.close()
    print(f"Architecture diagram generated: {output_path}")

if __name__ == "__main__":
    draw_architecture_diagram()
