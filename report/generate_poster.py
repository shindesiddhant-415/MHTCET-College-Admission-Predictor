"""
Production-grade Academic Conference Poster Generator
MIT Academy of Engineering | TY B.Tech. AIML Mini Project
Builds high-density, legible, publication-quality A3/A2 poster (PNG & PDF)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

OUTPUT_PNG = r"D:\AIML-PROJECT\report\project_poster.png"
OUTPUT_PDF = r"D:\AIML-PROJECT\report\project_poster.pdf"

# Image assets
ARCH_PATH = r"D:\AIML-PROJECT\report\screenshots\architecture_diagram.png"
PLOT_PATH = r"D:\AIML-PROJECT\report\screenshots\actual_vs_predicted.png"
APP_PATH = r"D:\AIML-PROJECT\report\screenshots\app_recommendations_tab.png"

def make_poster():
    print("Generating High-Legibility Academic Conference Poster...")
    
    # 24 x 14 inches canvas (16:9.33 conference poster ratio)
    fig = plt.figure(figsize=(24, 14), facecolor='#0b1329') # Dark Navy Poster Board
    
    # Root axis for background and header
    ax_root = fig.add_axes([0, 0, 1, 1])
    ax_root.set_xlim(0, 1000)
    ax_root.set_ylim(0, 1000)
    ax_root.axis('off')
    
    # Dark navy gradient background
    ax_root.add_patch(Rectangle((0, 0), 1000, 1000, facecolor='#0f172a', edgecolor='none', zorder=1))
    
    # -------------------------------------------------------------
    # 1. Header Banner (y: 865 to 985)
    # -------------------------------------------------------------
    header_box = FancyBboxPatch((15, 860), 970, 125, boxstyle="round,pad=0,rounding_size=12",
                                facecolor='#1e293b', edgecolor='#3b82f6', linewidth=2.5, zorder=2)
    ax_root.add_patch(header_box)
    
    # Accent top stripe
    stripe = FancyBboxPatch((15, 975), 970, 10, boxstyle="round,pad=0,rounding_size=5",
                            facecolor='#38bdf8', edgecolor='none', zorder=3)
    ax_root.add_patch(stripe)
    
    # University & Department text
    ax_root.text(500, 955, "MIT ACADEMY OF ENGINEERING, ALANDI (D), PUNE",
                 ha='center', va='center', fontsize=18, fontweight='bold', color='#60a5fa', zorder=4)
    ax_root.text(500, 936, "Department of Computer Engineering  |  Multidisciplinary Minor in AI & Machine Learning",
                 ha='center', va='center', fontsize=13, fontweight='medium', color='#cbd5e1', zorder=4)
    
    # Title
    ax_root.text(500, 908, "AI-Based MHT-CET College Admission Prediction & Personalized Recommendation System",
                 ha='center', va='center', fontsize=21, fontweight='bold', color='#ffffff', zorder=4)
    
    # Authors & Academic details
    authors = "Student Researchers: Dipti Patil (202401040161)  |  Rohan Burande (202401040188)  |  Samadhan Kendhale (202401040243)  |  Siddhant Shinde (202401040250)"
    ax_root.text(500, 882, authors, ha='center', va='center', fontsize=12.5, fontweight='bold', color='#fde047', zorder=4)
    
    guide_meta = "Class: TY B.Tech. Comp (Div B, Batch B2)  |  Practical No. 07 (Mini Project)  |  Guide: AIML Faculty Coordinator  |  Nov 2026"
    ax_root.text(500, 866, guide_meta, ha='center', va='center', fontsize=11, color='#94a3b8', zorder=4)

    # -------------------------------------------------------------
    # Helper to build a Card Axis
    # -------------------------------------------------------------
    def create_card(x_norm, y_norm, w_norm, h_norm, title, tag=""):
        # Card outer boundary patch on root
        x_pt = x_norm * 1000
        y_pt = y_norm * 1000
        w_pt = w_norm * 1000
        h_pt = h_norm * 1000
        
        card_bg = FancyBboxPatch((x_pt, y_pt), w_pt, h_pt, boxstyle="round,pad=0,rounding_size=10",
                                 facecolor='#ffffff', edgecolor='#334155', linewidth=1.5, zorder=2)
        ax_root.add_patch(card_bg)
        
        # Header banner inside card
        header_h = 32
        card_header = FancyBboxPatch((x_pt, y_pt + h_pt - header_h), w_pt, header_h,
                                     boxstyle="round,pad=0,rounding_size=10",
                                     facecolor='#00296b', edgecolor='none', zorder=3)
        ax_root.add_patch(card_header)
        # Square off bottom of header
        ax_root.add_patch(Rectangle((x_pt, y_pt + h_pt - header_h), w_pt, 12, facecolor='#00296b', zorder=3))
        
        # Title text
        ax_root.text(x_pt + 15, y_pt + h_pt - 16, title,
                     ha='left', va='center', fontsize=13, fontweight='bold', color='#ffffff', zorder=4)
        if tag:
            ax_root.text(x_pt + w_pt - 15, y_pt + h_pt - 16, tag,
                         ha='right', va='center', fontsize=10.5, fontweight='bold', color='#fde047', zorder=4)
        
        # Create sub-axis for inner content
        pad_x = 0.008
        pad_y = 0.008
        h_content = h_norm - 0.038
        ax_content = fig.add_axes([x_norm + pad_x, y_norm + pad_y, w_norm - (2 * pad_x), h_content])
        ax_content.set_xlim(0, 100)
        ax_content.set_ylim(0, 100)
        ax_content.axis('off')
        return ax_content

    # -------------------------------------------------------------
    # COLUMN 1: x = 0.015, width = 0.31
    # -------------------------------------------------------------
    # Card 1: Problem Statement & SDG Alignment
    ax1 = create_card(0.015, 0.605, 0.31, 0.245, "1. Problem Statement & SDG Alignment", "SDG 4 & 10")
    p1_lines = [
        ("• Admission Challenge:", True, "#0f172a", 12),
        ("  Over 140,000 engineering aspirants in Maharashtra face high", False, "#334155", 11.5),
        ("  uncertainty analyzing historical closing cutoffs published across", False, "#334155", 11.5),
        ("  disjoint, multi-page regulatory PDF documents across rounds & quotas.", False, "#334155", 11.5),
        ("• Information Asymmetry & Seat Forfeiture:", True, "#0f172a", 12),
        ("  Complex category reservations (GOPENS, GOBCS, GSCS, TFWS, EWS)", False, "#334155", 11.5),
        ("  and shifting seat intake cause suboptimal choice formulation.", False, "#334155", 11.5),
        ("• Proposed Solution:", True, "#00296b", 12),
        ("  An AI decision-support platform predicting future closing percentiles", False, "#334155", 11.5),
        ("  with explainable Safer, Moderate, and Reach suitability recommendations.", False, "#334155", 11.5),
        ("• UN SDG Mapping:", True, "#047857", 12),
        ("  - SDG 4 (Quality Education): Transparent admission guidance for all.", False, "#065f46", 11.5),
        ("  - SDG 10 (Reduced Inequalities): Equal access for rural & reserved quotas.", False, "#065f46", 11.5),
    ]
    cur_y = 92
    for text, bold, color, size in p1_lines:
        ax1.text(2, cur_y, text, ha='left', va='top', fontsize=size,
                 fontweight='bold' if bold else 'normal', color=color)
        cur_y -= 7.3

    # Card 2: Data Engineering & Official Documents
    ax2 = create_card(0.015, 0.320, 0.31, 0.275, "2. Data Ingestion & Engineering Pipeline", "32,144 Records")
    p2_lines = [
        ("• Official Regulatory Ingestion (18 Documents):", True, "#0f172a", 12),
        ("  - Cutoffs: CAP Rounds I, II, III for AY 2023-24 to 2026-27 (12 PDFs)", False, "#334155", 11.5),
        ("  - Seat Matrices: Sanctioned annual intake for AY 2023-27 (6 PDFs)", False, "#334155", 11.5),
        ("• Automated Extraction Pipeline:", True, "#0f172a", 12),
        ("  - PyMuPDF text stream extraction + DTE course regex parsing.", False, "#334155", 11.5),
        ("  - Extracted 32,144 cutoff records & 704 sanctioned intake rows.", False, "#334155", 11.5),
        ("  - Handled 14 quota categories with Stage I / Stage II resolution.", False, "#334155", 11.5),
        ("• Data Cleaning Safeguards:", True, "#00296b", 12),
        ("  - Zero downward bias: Unallocated seats never imputed with 0.0.", False, "#334155", 11.5),
        ("  - Mid-page split resolution via 10-digit DTE code backfill.", False, "#334155", 11.5),
        ("  - 100% verified percentiles (0 <= p <= 100) and merit rank > 0.", False, "#334155", 11.5),
    ]
    cur_y = 92
    for text, bold, color, size in p2_lines:
        ax2.text(2, cur_y, text, ha='left', va='top', fontsize=size,
                 fontweight='bold' if bold else 'normal', color=color)
        cur_y -= 7.4

    # Card 3: System Architecture
    ax3 = create_card(0.015, 0.040, 0.31, 0.270, "3. End-to-End System Architecture", "FastAPI + React 18")
    if os.path.exists(ARCH_PATH):
        arch_img = mpimg.imread(ARCH_PATH)
        ax3.imshow(arch_img, extent=[0, 100, 0, 95], aspect='auto')

    # -------------------------------------------------------------
    # COLUMN 2: x = 0.340, width = 0.32
    # -------------------------------------------------------------
    # Card 4: Feature Store & Anti-Leakage
    ax4 = create_card(0.340, 0.635, 0.32, 0.215, "4. Chronological Split & Feature Store", "Strict No-Leakage")
    p4_lines = [
        ("• Expanding-Window Temporal Split:", True, "#0f172a", 12),
        ("  - Training & Validation: Academic Years 2023-24 to 2025-26 (24,108 rows)", False, "#334155", 11.5),
        ("  - Out-of-Time Held-Out Test: Academic Year 2026-27 (8,036 rows)", False, "#334155", 11.5),
        ("• Engineered Chronological Features:", True, "#00296b", 12),
        ("  - cutoff_lag_1yr, cutoff_lag_2yr: Multi-year autoregressive closing lags.", False, "#334155", 11.5),
        ("  - yoy_cutoff_diff: Year-over-year directional velocity & momentum.", False, "#334155", 11.5),
        ("  - total_intake, state_seats: Institutional capacity & quota shifts.", False, "#334155", 11.5),
        ("  - OneHotEncoder(handle_unknown='ignore') for college, branch, quota.", False, "#334155", 11.5),
    ]
    cur_y = 92
    for text, bold, color, size in p4_lines:
        ax4.text(2, cur_y, text, ha='left', va='top', fontsize=size,
                 fontweight='bold' if bold else 'normal', color=color)
        cur_y -= 10.2

    # Card 5: ML Benchmark Leaderboard
    ax5 = create_card(0.340, 0.320, 0.32, 0.305, "5. ML Algorithm Benchmarking Leaderboard", "Held-Out 2026-27")
    
    # Leaderboard table headers
    ax5.text(2, 92, "Held-Out Test Set (AY 2026-27, N=8,036):", fontsize=11.5, fontweight='bold', color='#0f172a')
    
    t_headers = ["Algorithm", "MAE ↓", "RMSE ↓", "R² ↑", "Fit", "Status"]
    col_x = [2, 38, 52, 66, 80, 91]
    
    # Table header bar
    ax5.add_patch(Rectangle((1, 80), 98, 8, facecolor='#00296b', edgecolor='none'))
    for h_i, h_txt in enumerate(t_headers):
        ax5.text(col_x[h_i], 84, h_txt, ha='left' if h_i == 0 else 'center', va='center',
                 fontsize=10.5, fontweight='bold', color='#ffffff')
        
    t_rows = [
        ("Ridge Regression (SGD/L2)", "0.1133", "0.1415", "0.9996", "0.12s", "BEST", True),
        ("Random Forest Regressor", "0.1168", "0.1442", "0.9996", "1.30s", "Eval", False),
        ("HistGradientBoosting", "0.1236", "0.1612", "0.9994", "3.63s", "Eval", False),
        ("Decision Tree Regressor", "0.1266", "0.1574", "0.9995", "0.21s", "Eval", False),
        ("Previous-Year Baseline", "0.2037", "0.2346", "0.9988", "<0.01s", "Naive", False)
    ]
    
    row_y = 73
    for r_i, (model_name, mae, rmse, r2, fit_t, stat, is_best) in enumerate(t_rows):
        bg_col = "#dcfce7" if is_best else ("#f8fafc" if r_i % 2 == 1 else "#ffffff")
        ax5.add_patch(Rectangle((1, row_y - 2), 98, 7.5, facecolor=bg_col, edgecolor='#cbd5e1', linewidth=0.5))
        
        font_wt = 'bold' if is_best else 'normal'
        t_col = '#047857' if is_best else '#0f172a'
        
        ax5.text(col_x[0], row_y + 1.8, model_name, fontsize=10, fontweight=font_wt, color=t_col)
        ax5.text(col_x[1], row_y + 1.8, mae, ha='center', fontsize=10, fontweight=font_wt, color=t_col)
        ax5.text(col_x[2], row_y + 1.8, rmse, ha='center', fontsize=10, fontweight=font_wt, color=t_col)
        ax5.text(col_x[3], row_y + 1.8, r2, ha='center', fontsize=10, fontweight=font_wt, color=t_col)
        ax5.text(col_x[4], row_y + 1.8, fit_t, ha='center', fontsize=9.5, color='#475569')
        ax5.text(col_x[5], row_y + 1.8, stat, ha='center', fontsize=9.5, fontweight='bold', color=t_col)
        row_y -= 8.2

    b_text = (
        "• Winning Selection: Ridge Regression with L2 Regularization (alpha=10.0).\n"
        "• 44.4% Error Reduction over naive prior-year copying (MAE: 0.1133 vs 0.2037).\n"
        "• Sub-Second Latency: 120 ms fit and 27 ms inference for real-time recommendations."
    )
    ax5.text(2, 23, b_text, fontsize=10.8, color='#0f172a', linespacing=1.35)

    # Card 6: Model Diagnostics Plot
    ax6 = create_card(0.340, 0.040, 0.32, 0.270, "6. Model Diagnostics: Actual vs Predicted", "R² = 0.9996")
    if os.path.exists(PLOT_PATH):
        plot_img = mpimg.imread(PLOT_PATH)
        ax6.imshow(plot_img, extent=[0, 100, 0, 95], aspect='auto')

    # -------------------------------------------------------------
    # COLUMN 3: x = 0.675, width = 0.31
    # -------------------------------------------------------------
    # Card 7: Recommendation Engine & Safety Margin
    ax7 = create_card(0.675, 0.635, 0.31, 0.215, "7. Personalized Recommendation Logic", "Explainable AI")
    p7_lines = [
        ("• Transparent Percentile Gap Formula:", True, "#00296b", 12),
        ("  Delta = P_candidate - y_hat_cutoff", True, "#0f172a", 12.5),
        ("• Dynamic Validation Error Safety Margin:", True, "#00296b", 12),
        ("  M = 1.5 * MAE ≈ 0.170 percentile points", True, "#047857", 12),
        ("• 3-Tier Admission Suitability Classification:", True, "#0f172a", 12),
        ("  [+] Safer (Delta >= +M): Candidate percentile comfortably clears cutoff.", False, "#065f46", 11),
        ("  [~] Moderate (-M <= Delta < +M): Competitive boundary; solid viable target.", False, "#b45309", 11),
        ("  [-] Reach (Delta < -M): Aspirational choice; strategic reach option.", False, "#b91c1c", 11),
    ]
    cur_y = 92
    for text, bold, color, size in p7_lines:
        ax7.text(2, cur_y, text, ha='left', va='top', fontsize=size,
                 fontweight='bold' if bold else 'normal', color=color)
        cur_y -= 10.3

    # Card 8: Live Full-Stack Deployed Web Application
    ax8 = create_card(0.675, 0.320, 0.31, 0.305, "8. Full-Stack Deployed Web Application", "Render Cloud Live")
    if os.path.exists(APP_PATH):
        app_img = mpimg.imread(APP_PATH)
        ax8.imshow(app_img, extent=[0, 100, 32, 97], aspect='auto')
    
    deploy_info = (
        "• Stack: Modern React 18 SPA (Vite) + FastAPI ASGI Backend.\n"
        "• Live URL: https://mhtcet-college-admission-predictor.onrender.com\n"
        "• Features: Multi-year trends, college comparison, CSV exports."
    )
    ax8.text(2, 24, deploy_info, fontsize=10.5, color='#0f172a', linespacing=1.3)

    # Card 9: Automated Testing & Deliverables Compliance
    ax9 = create_card(0.675, 0.040, 0.31, 0.270, "9. Automated Testing & Verification", "20/20 Pytest Pass")
    p9_lines = [
        ("• Pytest Automated Test Suite (100% Pass Rate):", True, "#0f172a", 12),
        ("  - 20 unit, integration & API test cases across TC-1 to TC-5.", False, "#334155", 11),
        ("  - Data integrity, range bounds, non-leakage & model latency.", False, "#334155", 11),
        ("• Academic Syllabus Deliverables Checklist:", True, "#00296b", 12),
        ("  [OK] Well-commented Source code & 6 Jupyter notebooks (01-06)", False, "#065f46", 11),
        ("  [OK] Comprehensive README.md with setup & execution guide", False, "#065f46", 11),
        ("  [OK] 18 Ingested CET PDFs & Normalized CSV feature stores", False, "#065f46", 11),
        ("  [OK] requirements.txt dependency specifications", False, "#065f46", 11),
        ("  [OK] Saved production model: selected_model.joblib + metadata", False, "#065f46", 11),
        ("  [OK] High-resolution UI screenshots & model diagnostics", False, "#065f46", 11),
        ("  [OK] Formal Project Report (PDF/DOCX) & Academic Poster", False, "#065f46", 11),
    ]
    cur_y = 92
    for text, bold, color, size in p9_lines:
        ax9.text(2, cur_y, text, ha='left', va='top', fontsize=size,
                 fontweight='bold' if bold else 'normal', color=color)
        cur_y -= 7.4

    # -------------------------------------------------------------
    # Footer Banner (y: 10 to 30)
    # -------------------------------------------------------------
    ax_root.text(500, 18, "MIT Academy of Engineering | TY B.Tech. Computer Engineering (MDM AI & ML) | Practical No. 07 Mini-Project",
                 ha='center', va='center', fontsize=11, color='#64748b', zorder=4)

    # Save at 200 DPI for PNG (giving crisp 4800 x 2800 resolution) and PDF
    print("Saving PNG & PDF...")
    plt.savefig(OUTPUT_PNG, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(OUTPUT_PDF, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    
    png_size = os.path.getsize(OUTPUT_PNG)
    pdf_size = os.path.getsize(OUTPUT_PDF)
    print(f"[OK] High-legibility poster saved successfully!")
    print(f"  PNG: {OUTPUT_PNG} ({png_size:,} bytes)")
    print(f"  PDF: {OUTPUT_PDF} ({pdf_size:,} bytes)")

if __name__ == "__main__":
    make_poster()
