"""
Script to generate the Academic Project Poster Photograph (PNG and PDF)
for the MITAOE TY B.Tech AIML Mini Project.
Resolution: 300 DPI, High-definition Academic Conference Poster format.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np

OUTPUT_PNG = r"D:\AIML-PROJECT\report\project_poster.png"
OUTPUT_PDF = r"D:\AIML-PROJECT\report\project_poster.pdf"

def generate_poster():
    print("Generating Academic Project Poster...")
    
    # 16:9 widescreen or standard A3/A2 landscape ratio: 24 x 13.5 inches at 200/300 DPI
    fig = plt.figure(figsize=(24, 13.5), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    # Background color
    bg_color = "#f8fafc" # slate-50
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    # Palette
    c_primary = "#00296b"     # Deep Oxford Navy
    c_secondary = "#00509d"   # MIT Blue
    c_accent = "#ffd166"      # Warm Gold
    c_card_bg = "#ffffff"     # White Card
    c_border = "#cbd5e1"      # Border slate
    c_text_dark = "#0f172a"   # Dark slate
    c_text_muted = "#475569"  # Muted slate
    c_success = "#059669"     # Emerald Green
    
    # -------------------------------------------------------------
    # 1. Header Banner
    # -------------------------------------------------------------
    header_rect = FancyBboxPatch((0.02, 0.86), 0.96, 0.125, boxstyle="round,pad=0.01,rounding_size=0.015",
                                 facecolor=c_primary, edgecolor="#001845", linewidth=2, zorder=2)
    ax.add_patch(header_rect)
    
    # Sub-header gold stripe
    stripe = FancyBboxPatch((0.02, 0.852), 0.96, 0.008, boxstyle="square,pad=0",
                            facecolor=c_accent, edgecolor="none", zorder=3)
    ax.add_patch(stripe)
    
    # College info
    ax.text(0.5, 0.965, "MIT ACADEMY OF ENGINEERING, ALANDI (D), PUNE - 412105",
            ha='center', va='center', fontsize=15, fontweight='bold', color='#93c5fd', zorder=4)
    ax.text(0.5, 0.945, "Department of Computer Engineering | Multidisciplinary Minor in AI & Machine Learning",
            ha='center', va='center', fontsize=12, color='#e2e8f0', zorder=4)
    
    # Title
    ax.text(0.5, 0.915, "AI-Based MHT-CET College Admission Prediction and Personalized Recommendation System",
            ha='center', va='center', fontsize=21, fontweight='bold', color='#ffffff', zorder=4)
    
    # Team & Meta
    authors_text = "Student Researchers: Dipti Patil (202401040161)  |  Rohan Burande (202401040188)  |  Samadhan Kendhale (202401040243)  |  Siddhant Shinde (202401040250)"
    guide_text = "Class: TY B.Tech. Comp (Div B, Batch B2)  |  Guide: AIML Project Faculty Coordinator  |  Academic Year: 2026-27"
    ax.text(0.5, 0.885, authors_text, ha='center', va='center', fontsize=11, fontweight='bold', color=c_accent, zorder=4)
    ax.text(0.5, 0.867, guide_text, ha='center', va='center', fontsize=10.5, color='#cbd5e1', zorder=4)
    
    # Helper to draw card boxes
    def draw_card(x, y, w, h, title, prefix="§"):
        card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.012",
                              facecolor=c_card_bg, edgecolor=c_border, linewidth=1.5, zorder=2)
        ax.add_patch(card)
        # Card header pill
        header_pill = FancyBboxPatch((x, y + h - 0.038), w, 0.038, boxstyle="round,pad=0.005,rounding_size=0.01",
                                     facecolor="#f1f5f9", edgecolor="none", zorder=3)
        ax.add_patch(header_pill)
        # Title text
        ax.text(x + 0.015, y + h - 0.019, f"{prefix}  {title}", ha='left', va='center',
                fontsize=13, fontweight='bold', color=c_primary, zorder=4)

    # -------------------------------------------------------------
    # COLUMN 1 (Left: x = 0.02 to 0.33)
    # -------------------------------------------------------------
    # 1. Problem & SDG
    draw_card(0.02, 0.60, 0.31, 0.235, "Problem Statement & SDG Alignment", "[1]")
    prob_p1 = (
        "• Challenge: 140,000+ Maharashtra engineering aspirants must submit prioritized\n"
        "  option lists across 300+ colleges and 4 CAP rounds. Official cutoffs are\n"
        "  distributed across disjoint, unstructured multi-page PDF documents.\n"
        "• Consequence: Severe information asymmetry, quota complexity (GOPENS, GOBCS,\n"
        "  GSCS, GSTS, TFWS, EWS), seat forfeiture, and suboptimal choice selection.\n"
        "• Solution: An end-to-end AI pipeline extracting official cutoffs, predicting future\n"
        "  closing thresholds via regression, and generating explainable candidate option lists.\n"
        "• UN SDG Alignment:\n"
        "   - SDG 4 (Quality Education): Democratizes equitable admission guidance.\n"
        "   - SDG 10 (Reduced Inequalities): Equalizes access for rural & non-metro students."
    )
    ax.text(0.032, 0.705, prob_p1, ha='left', va='center', fontsize=10.5, color=c_text_dark, linespacing=1.45, zorder=4)

    # 2. Pipeline & Ingestion
    draw_card(0.02, 0.32, 0.31, 0.265, "Data Engineering & CET Documents", "[2]")
    data_p = (
        "• Official CET Source Manifest (18 Regulatory Documents Ingested):\n"
        "   - Cutoffs: CAP Rounds I, II, III for AY 2023-24, 2024-25, 2025-26, 2026-27 (12 PDFs)\n"
        "   - Seat Matrix: Sanctioned seat matrices across 2023-2027 (6 PDFs)\n"
        "• Parsing Pipeline:\n"
        "   - PDFPlumber multi-stage extraction + 10-digit DTE course regex normalization.\n"
        "   - 32,144 structured cutoff records & 704 sanctioned seat matrix rows.\n"
        "   - Category extraction for 14 quota classifications with Stage I/II resolution.\n"
        "• Quality Assurance & Auditability:\n"
        "   - 0 missing critical values, 100% official DTE code linkage.\n"
        "   - SHA-256 cryptographic provenance logged for every ingested document."
    )
    ax.text(0.032, 0.445, data_p, ha='left', va='center', fontsize=10.5, color=c_text_dark, linespacing=1.4, zorder=4)

    # 3. System Architecture Diagram
    draw_card(0.02, 0.03, 0.31, 0.275, "End-to-End System Architecture", "[3]")
    arch_img_path = r"D:\AIML-PROJECT\report\screenshots\architecture_diagram.png"
    if os.path.exists(arch_img_path):
        arch_img = mpimg.imread(arch_img_path)
        ax.imshow(arch_img, extent=[0.025, 0.325, 0.038, 0.262], aspect='auto', zorder=4)

    # -------------------------------------------------------------
    # COLUMN 2 (Center: x = 0.345 to 0.655)
    # -------------------------------------------------------------
    # 4. Feature Engineering & Chronological Evaluation
    draw_card(0.345, 0.63, 0.31, 0.205, "Feature Store & Chronological Split", "[4]")
    feat_p = (
        "• Chronological Validation Strategy (Strict Anti-Leakage):\n"
        "   - Training & Tuning: Academic Years 2023-24 to 2025-26 (24,108 samples)\n"
        "   - Out-of-Time Held-Out Test: Academic Year 2026-27 (8,036 samples)\n"
        "• Engineered Feature Representations:\n"
        "   - cutoff_lag_1yr, cutoff_lag_2yr: Rolling closing percentiles\n"
        "   - yoy_cutoff_diff: Directional cutoff velocity and annual shift\n"
        "   - total_intake, state_seats, minority_seats: Seat capacity features\n"
        "   - High-cardinality Target & Frequency encoding for college and branch."
    )
    ax.text(0.357, 0.725, feat_p, ha='left', va='center', fontsize=10.5, color=c_text_dark, linespacing=1.45, zorder=4)

    # 5. ML Benchmark Leaderboard
    draw_card(0.345, 0.32, 0.31, 0.295, "Machine Learning Algorithm Benchmark", "[5]")
    leaderboard_data = [
        ["Model Architecture", "MAE ↓", "RMSE ↓", "R² ↑", "Fit Time", "Status"],
        ["Ridge Regression (SGD/L2)", "0.1133", "0.1415", "0.9996", "0.12 s", "SELECTED"],
        ["Random Forest Regressor", "0.1168", "0.1442", "0.9996", "1.30 s", "Evaluated"],
        ["HistGradientBoosting", "0.1236", "0.1612", "0.9994", "3.63 s", "Evaluated"],
        ["Decision Tree Regressor", "0.1266", "0.1574", "0.9995", "0.21 s", "Evaluated"],
        ["Previous-Year Baseline", "0.2037", "0.2346", "0.9988", "0.001 s", "Naive Ref."]
    ]
    
    # Draw custom high-contrast table
    t_x, t_y, t_w, t_h = 0.355, 0.445, 0.29, 0.13
    col_w = [0.115, 0.035, 0.035, 0.035, 0.035, 0.035]
    row_h = t_h / len(leaderboard_data)
    
    for r_i, row in enumerate(leaderboard_data):
        curr_y = t_y + t_h - (r_i + 1) * row_h
        row_bg = c_primary if r_i == 0 else ("#dcfce7" if r_i == 1 else ("#f8fafc" if r_i % 2 == 1 else "#ffffff"))
        rect_row = FancyBboxPatch((t_x, curr_y), t_w, row_h, boxstyle="square,pad=0",
                                  facecolor=row_bg, edgecolor="#e2e8f0", linewidth=0.5, zorder=4)
        ax.add_patch(rect_row)
        
        c_curr_x = t_x + 0.005
        for c_i, cell in enumerate(row):
            txt_color = "#ffffff" if r_i == 0 else (c_success if (r_i == 1 and c_i == 5) else c_text_dark)
            font_wt = 'bold' if (r_i == 0 or r_i == 1 or c_i == 0) else 'normal'
            align = 'left' if c_i == 0 else 'center'
            cell_x = c_curr_x + 0.002 if align == 'left' else c_curr_x + col_w[c_i] / 2
            ax.text(cell_x, curr_y + row_h / 2, cell, ha=align, va='center',
                    fontsize=9.5, fontweight=font_wt, color=txt_color, zorder=5)
            c_curr_x += col_w[c_i]

    bench_summary = (
        "• Winning Selection: Ridge Regression achieved 0.1133% MAE (44.4% error reduction\n"
        "  over naive baseline). L2 regularization prevents overfitting on collinear lags.\n"
        "• Extreme Speed: 120 ms training and 27 ms inference ensures sub-second responses."
    )
    ax.text(0.357, 0.365, bench_summary, ha='left', va='center', fontsize=10.5, color=c_text_dark, linespacing=1.4, zorder=4)

    # 6. Benchmark Diagnostic Plot
    draw_card(0.345, 0.03, 0.31, 0.275, "Diagnostic Plots: Actual vs Predicted", "[6]")
    plot_path = r"D:\AIML-PROJECT\report\screenshots\actual_vs_predicted.png"
    if os.path.exists(plot_path):
        plot_img = mpimg.imread(plot_path)
        ax.imshow(plot_img, extent=[0.350, 0.650, 0.038, 0.262], aspect='auto', zorder=4)

    # -------------------------------------------------------------
    # COLUMN 3 (Right: x = 0.67 to 0.98)
    # -------------------------------------------------------------
    # 7. Recommendation Engine & Suitability Margin
    draw_card(0.67, 0.63, 0.31, 0.205, "Personalized Recommendation Engine", "[7]")
    rec_p = (
        "• Transparent Percentile Gap Formulation:  delta = P_student - y_hat\n"
        "• Dynamic Safety Margin:  M = 1.5 * MAE ≈ 0.170%\n"
        "• 3-Tier Admission Suitability Classification:\n"
        "   (+) Safer (delta >= +M): Candidate score comfortably clears predicted cutoff.\n"
        "   (~) Moderate (-M <= delta < +M): Competitive boundary; solid viable target.\n"
        "   (-) Reach (delta < -M): Aspirational reach; realistic stretch choice.\n"
        "• Eliminates Black-Box Opacity: Every recommendation includes exact percentile\n"
        "  buffer, historical closing trends, and seat capacity breakdown."
    )
    ax.text(0.682, 0.725, rec_p, ha='left', va='center', fontsize=10.5, color=c_text_dark, linespacing=1.45, zorder=4)

    # 8. React 18 Application & Live Deployed Service
    draw_card(0.67, 0.32, 0.31, 0.295, "Live Full-Stack Deployment (React 18 + FastAPI)", "[8]")
    
    app_img_path = r"D:\AIML-PROJECT\report\screenshots\app_recommendations_tab.png"
    if os.path.exists(app_img_path):
        app_img = mpimg.imread(app_img_path)
        ax.imshow(app_img, extent=[0.675, 0.975, 0.405, 0.575], aspect='auto', zorder=4)

    deploy_p = (
        "• React 18 Single-Page Application: Modular tabbed interface built with Vite,\n"
        "  featuring interactive filters, responsive cards, and dynamic sorting.\n"
        "• FastAPI REST ML Service: High-throughput async backend with Pydantic validation.\n"
        "• Worldwide Cloud Hosting: Live on Render with automated CI/CD pipeline.\n"
        "• Live Production URL: https://mhtcet-college-admission-predictor.onrender.com"
    )
    ax.text(0.682, 0.360, deploy_p, ha='left', va='center', fontsize=10.5, color=c_text_dark, linespacing=1.35, zorder=4)

    # 9. Verification, Quality & Project Outcomes
    draw_card(0.67, 0.03, 0.31, 0.275, "Verification, Testing & Key Deliverables", "[9]")
    outcomes_p = (
        "• Automated Test Suite: 20 / 20 Pytest unit & API tests passing (100% pass rate).\n"
        "• Real-World Validation: Validated on 32,144 official cutoff points (2023–2027).\n"
        "• Reproducibility: Full Git repository with clean source, dataset manifests,\n"
        "  6 step-by-step Jupyter notebooks, serialized models, and requirements.txt.\n"
        "• Academic Project Repository Deliverables Checklist:\n"
        "   [OK] Source Code / Jupyter Notebooks (well-commented from student POV)\n"
        "   [OK] Comprehensive README.md with architecture and setup instructions\n"
        "   [OK] Normalized Dataset & official CET Cell provenance links\n"
        "   [OK] requirements.txt dependency specifications\n"
        "   [OK] Serialized trained model (selected_model.joblib + metadata.json)\n"
        "   [OK] UI Screenshots & Model Benchmark Diagnostic Plots\n"
        "   [OK] Formal Project Report (PDF/DOCX) & High-Resolution Conference Poster"
    )
    ax.text(0.682, 0.162, outcomes_p, ha='left', va='center', fontsize=10.2, color=c_text_dark, linespacing=1.4, zorder=4)

    # -------------------------------------------------------------
    # Footer Banner
    # -------------------------------------------------------------
    footer_rect = FancyBboxPatch((0.02, 0.005), 0.96, 0.020, boxstyle="round,pad=0.002,rounding_size=0.005",
                                 facecolor="#1e293b", edgecolor="none", zorder=3)
    ax.add_patch(footer_rect)
    ax.text(0.5, 0.015, "MIT Academy of Engineering | TY B.Tech. Mini Project Practical No. 07 | Live URL: https://mhtcet-college-admission-predictor.onrender.com",
            ha='center', va='center', fontsize=10, color='#94a3b8', zorder=4)

    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(OUTPUT_PDF, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    
    print(f"[OK] Poster successfully saved to:\n  - {OUTPUT_PNG}\n  - {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_poster()
