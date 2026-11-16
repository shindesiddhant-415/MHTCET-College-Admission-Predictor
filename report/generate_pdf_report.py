"""
Script to generate the comprehensive, official MITAOE Academic Project Report PDF
using ReportLab 5.0.
Output: report/final_report.pdf and report/project_report.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_OUTPUT_1 = r"D:\AIML-PROJECT\report\final_report.pdf"
PDF_OUTPUT_2 = r"D:\AIML-PROJECT\report\project_report.pdf"

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw total page numbers and running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#475569"))
            
            # Running Header
            self.drawString(54, 842 - 36, "MIT Academy of Engineering | TY B.Tech. Computer Engineering (MDM AI & ML)")
            self.drawRightString(595 - 54, 842 - 36, "Mini Project Practical No. 07")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 842 - 42, 595 - 54, 842 - 42)
            
            # Running Footer
            self.line(54, 46, 595 - 54, 46)
            self.drawString(54, 32, "MHT-CET Admission Prediction & Personalized Recommendation System")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(595 - 54, 32, page_text)
            self.restoreState()


def build_pdf_report():
    print("Building Official Project Report PDF...")
    doc = SimpleDocTemplate(
        PDF_OUTPUT_1,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#00296b"),
        alignment=1, # Center
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#334155"),
        alignment=1,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'ChapterH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#00296b"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#00509d"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # -------------------------------------------------------------
    # 1. Title Page / Cover Section
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("MIT ACADEMY OF ENGINEERING, PUNE", ParagraphStyle('UnivHeader', parent=title_style, fontSize=14, leading=17, textColor=colors.HexColor("#00296b"))))
    story.append(Paragraph("(An Autonomous Institute Affiliated to Savitribai Phule Pune University)<br/>Alandi (D), Pune - 412105, Maharashtra, India", subtitle_style))
    story.append(Paragraph("DEPARTMENT OF COMPUTER ENGINEERING", ParagraphStyle('DeptHeader', parent=title_style, fontSize=12, leading=15, textColor=colors.HexColor("#00509d"))))
    story.append(Paragraph("Multidisciplinary Minor in Artificial Intelligence & Machine Learning (MDM AI & ML)", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#00296b"), spaceAfter=15))

    story.append(Paragraph("MINI PROJECT REPORT (PRACTICAL NO. 07)", ParagraphStyle('PracTag', parent=title_style, fontSize=12, leading=15, textColor=colors.HexColor("#d97706"))))
    story.append(Spacer(1, 5))
    story.append(Paragraph("AI-Based MHT-CET College Admission Prediction and Personalized Recommendation System", title_style))
    story.append(Paragraph("An End-to-End Decision-Support Platform Utilizing Multi-Year Cutoff Forecasting and Explainable Candidate Guidance", subtitle_style))
    story.append(Spacer(1, 10))

    # Group Details Table
    story.append(Paragraph("Project Team Details", h2_style))
    team_data = [
        [Paragraph("Sr.", table_header_style), Paragraph("Student Name", table_header_style), Paragraph("PRN", table_header_style), Paragraph("Roll", table_header_style), Paragraph("Project Role / Contribution", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("Dipti Patil", table_cell_bold), Paragraph("202401040161", table_cell_style), Paragraph("161", table_cell_style), Paragraph("Data Engineering Lead (PDF Extraction, Regex Normalization & Seat Matrix)", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("Rohan Burande", table_cell_bold), Paragraph("202401040188", table_cell_style), Paragraph("188", table_cell_style), Paragraph("Quality Analyst & Testing Lead (Data Validation, Pytest Suite & Source Traceability)", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("Samadhan Kendhale", table_cell_bold), Paragraph("202401040243", table_cell_style), Paragraph("243", table_cell_style), Paragraph("Full-Stack & Frontend Lead (React 18 SPA UI & FastAPI REST Backend)", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("Siddhant Shinde", table_cell_bold), Paragraph("202401040250", table_cell_style), Paragraph("250", table_cell_style), Paragraph("Lead ML & AI Engineer (Feature Engineering, Algorithm Benchmarking & Recommender)", table_cell_style)],
    ]
    t_team = Table(team_data, colWidths=[24, 85, 75, 32, 271])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00296b")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_team)
    story.append(Spacer(1, 10))

    # Academic Meta Table
    meta_data = [
        [Paragraph("Branch / Program:", table_cell_bold), Paragraph("B.Tech. Computer Engineering (MDM AI & ML)", table_cell_style), Paragraph("Academic Year:", table_cell_bold), Paragraph("2026–2027 (Semester V)", table_cell_style)],
        [Paragraph("Class & Batch:", table_cell_bold), Paragraph("TY - Division B / Batch B2", table_cell_style), Paragraph("Faculty Guide:", table_cell_bold), Paragraph("Prof. / Dr. AIML Lab Faculty Coordinator", table_cell_style)],
        [Paragraph("Course Code:", table_cell_bold), Paragraph("2311331L (AI & ML Lab)", table_cell_style), Paragraph("SDG Alignment:", table_cell_bold), Paragraph("SDG 4 (Quality Education) & SDG 10 (Reduced Inequalities)", table_cell_style)],
        [Paragraph("Live URL:", table_cell_bold), Paragraph("https://mhtcet-college-admission-predictor.onrender.com", table_cell_bold), Paragraph("Repository:", table_cell_bold), Paragraph("shindesiddhant-415/MHTCET-College-Admission-Predictor", table_cell_style)],
    ]
    t_meta = Table(meta_data, colWidths=[90, 160, 80, 157])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    # -------------------------------------------------------------
    # 2. Executive Abstract
    # -------------------------------------------------------------
    story.append(Paragraph("Executive Summary & Abstract", h1_style))
    p_abs1 = (
        "Students participating in the Maharashtra Centralized Admission Process (CAP) for undergraduate engineering "
        "admissions face substantial uncertainty navigating historical closing cutoffs distributed across disjoint PDF documents, "
        "admission rounds, seat categories, and institutions. This project develops an end-to-end AI-driven admission forecasting "
        "and recommendation system utilizing official Maharashtra State CET Cell documents across four academic years (2023–24 "
        "through 2026–27). A rigorous automated pipeline extracts, cleans, and normalizes 32,144 cutoff records and 704 seat matrix "
        "entries with complete source traceability."
    )
    p_abs2 = (
        "Five regression algorithms were implemented and chronologically evaluated on held-out test data (Year 2026–27): "
        "Previous-Year Baseline, Ridge Regression with L2 regularization, Decision Tree Regressor, Random Forest Regressor, and "
        "HistGradientBoosting Regressor. Ridge Regression achieved the highest predictive accuracy with a Mean Absolute Error "
        "(MAE) of 0.1133 percentile points, Root Mean Squared Error (RMSE) of 0.1415, and R² of 0.9996, vastly outperforming the "
        "previous-year baseline (MAE = 0.2037). A personalized recommendation engine leverages these forecasts to categorize "
        "eligible colleges into Safer, Moderate, and Reach options based on a transparent percentile-gap margin (M = 1.5 × MAE ≈ 0.170%). "
        "The system is deployed via a modern React 18 Single-Page Application (Vite) backed by a high-performance FastAPI REST "
        "ML service featuring multi-year trend analysis, head-to-head college comparison, automated unit testing (20/20 test pass rate), "
        "and complete source auditability."
    )
    story.append(Paragraph(p_abs1, body_style))
    story.append(Paragraph(p_abs2, body_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 3. Problem Statement & Motivation
    # -------------------------------------------------------------
    story.append(Paragraph("1. Problem Statement & Objectives", h1_style))
    story.append(Paragraph(
        "Every year, over 140,000 engineering aspirants in Maharashtra must prepare and submit prioritized college-branch option "
        "lists during the Centralized Admission Process (CAP). Official cutoff data is published solely as unstructured, high-volume "
        "PDF documents separated by academic year, CAP round, and seat category. Students and parents struggle to manually analyze "
        "year-over-year percentile movements, category-specific quota shifts (GOPENS, GOBCS, GSCS, GSTS, TFWS, EWS), and seat intake "
        "variations across hundreds of colleges. This information asymmetry frequently leads to suboptimal option list formulation, "
        "missed opportunities, or admission forfeiture.", body_style
    ))
    story.append(Paragraph("<b>Primary Project Objectives:</b>", body_style))
    story.append(Paragraph("• <b>Data Engineering:</b> Ingest and normalize 4 academic years of official Maharashtra CAP cutoff lists and seat matrices into a unified 32,144-record dataset.", bullet_style))
    story.append(Paragraph("• <b>Feature Engineering:</b> Construct leakage-free chronological lag features (t-1, t-2 cutoffs, cutoff momentum velocity, and seat intake changes) without future look-ahead.", bullet_style))
    story.append(Paragraph("• <b>Benchmarking:</b> Train, evaluate, and critically compare 5 regression algorithms using chronological expanding-window testing (Train: 2024, Val: 2025, Test: 2026).", bullet_style))
    story.append(Paragraph("• <b>Decision Support:</b> Formulate an explainable recommendation engine categorizing options into Safer, Moderate, and Reach options via dynamic error margins.", bullet_style))
    story.append(Paragraph("• <b>Full-Stack Deployment:</b> Deploy an interactive React 18 Single-Page Application (Vite) backed by a production FastAPI REST ML service with automated unit testing.", bullet_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 4. UN Sustainable Development Goals (SDG) Alignment
    # -------------------------------------------------------------
    story.append(Paragraph("2. UN Sustainable Development Goals (SDG) Alignment", h1_style))
    story.append(Paragraph(
        "This project directly maps to two critical United Nations Sustainable Development Goals (SDGs):", body_style
    ))
    story.append(Paragraph("• <b>SDG 4 (Quality Education):</b> By providing free, accessible, and transparent admission forecasting, the system empowers students from diverse socioeconomic backgrounds to make informed higher education choices, reducing reliance on expensive commercial counselling agents.", bullet_style))
    story.append(Paragraph("• <b>SDG 10 (Reduced Inequalities):</b> Centralized engineering admissions incorporate extensive reservation categories (SC, ST, OBC, EWS, TFWS, PWD, Defence). By explicitly modeling category quotas, the platform equalizes information access for rural and historically disadvantaged applicants.", bullet_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 5. Data Pipeline & Regulatory Source Ingestion
    # -------------------------------------------------------------
    story.append(Paragraph("3. Data Collection & Preprocessing Pipeline", h1_style))
    story.append(Paragraph(
        "A total of 18 regulatory documents published by the State Common Entrance Test Cell, Maharashtra State were systematically "
        "ingested across 4 academic years (2023–24 through 2026–27):", body_style
    ))
    
    src_data = [
        [Paragraph("Document Type", table_header_style), Paragraph("Academic Years Covered", table_header_style), Paragraph("CAP Rounds", table_header_style), Paragraph("Total Records", table_header_style), Paragraph("Integrity / Verification", table_header_style)],
        [Paragraph("CAP Cutoff Lists", table_cell_bold), Paragraph("2023–24, 2024–25, 2025–26, 2026–27", table_cell_style), Paragraph("Rounds I, II, III", table_cell_style), Paragraph("32,144 parsed entries", table_cell_style), Paragraph("100% valid percentiles (0–100)", table_cell_style)],
        [Paragraph("Sanctioned Seat Matrix", table_cell_bold), Paragraph("2023–24, 2024–25, 2025–26, 2026–27", table_cell_style), Paragraph("Annual Initial Matrix", table_cell_style), Paragraph("704 course rows", table_cell_style), Paragraph("Cross-verified with DTE portals", table_cell_style)],
        [Paragraph("Engineered ML Target", table_cell_bold), Paragraph("2024–25 to 2026–27 (with lags)", table_cell_style), Paragraph("CAP Round 1 Target", table_cell_style), Paragraph("22,960 target rows", table_cell_style), Paragraph("0 nulls across key features", table_cell_style)]
    ]
    t_src = Table(src_data, colWidths=[95, 115, 75, 85, 117])
    t_src.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00296b")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_src)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Rigorous Data Cleaning Safeguards:</b><br/>"
        "1. <b>Zero Downward Bias:</b> Unallocated seats are never imputed with 0.0, as 0.0 implies a candidate scored zero rather than unfilled quota.<br/>"
        "2. <b>Institute Code Resolution:</b> Mid-page PDF splits leaving orphan course blocks were resolved by deriving the 5-digit institute code directly from the 10-digit DTE course identifier.<br/>"
        "3. <b>Categorical Encoding:</b> Scikit-learn ColumnTransformer utilizes OneHotEncoder(handle_unknown='ignore') to ensure consistent matrix dimensionality across training and inference.", body_style
    ))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 6. System Architecture Diagram
    # -------------------------------------------------------------
    story.append(Paragraph("4. System Architecture", h1_style))
    story.append(Paragraph(
        "The end-to-end architecture integrates automated data extraction, feature store construction, chronological ML model "
        "training, a personalized recommendation engine, and a modern decoupled web interface:", body_style
    ))
    arch_path = r"D:\AIML-PROJECT\report\screenshots\architecture_diagram.png"
    if os.path.exists(arch_path):
        story.append(Image(arch_path, width=6.5*inch, height=3.2*inch))
        story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 7. Machine Learning Methodology & Benchmarking
    # -------------------------------------------------------------
    story.append(Paragraph("5. Machine Learning Benchmarking & Model Selection", h1_style))
    story.append(Paragraph(
        "To satisfy the academic curriculum requirements (P3 Linear Regression/Gradient Descent, P4 Decision Tree, P5 Ensembles), "
        "five distinct regression architectures were evaluated under a strict chronological expanding-window split:<br/>"
        "• <b>Training & Hyperparameter Tuning Window:</b> Academic Years 2023–24 to 2025–26 (24,108 samples)<br/>"
        "• <b>Held-Out Out-of-Time Test Window:</b> Academic Year 2026–27 (8,036 target samples)", body_style
    ))

    # Benchmark Table
    bench_data = [
        [Paragraph("Model Architecture", table_header_style), Paragraph("MAE (pts) ↓", table_header_style), Paragraph("MSE ↓", table_header_style), Paragraph("RMSE ↓", table_header_style), Paragraph("R² Score ↑", table_header_style), Paragraph("Fit Time", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("Ridge Regression (SGD/L2)", table_cell_bold), Paragraph("0.1133", table_cell_bold), Paragraph("0.0200", table_cell_bold), Paragraph("0.1415", table_cell_bold), Paragraph("0.9996", table_cell_bold), Paragraph("0.120 s", table_cell_style), Paragraph("SELECTED", table_cell_bold)],
        [Paragraph("Random Forest Regressor", table_cell_style), Paragraph("0.1168", table_cell_style), Paragraph("0.0208", table_cell_style), Paragraph("0.1442", table_cell_style), Paragraph("0.9996", table_cell_style), Paragraph("1.296 s", table_cell_style), Paragraph("Evaluated", table_cell_style)],
        [Paragraph("HistGradientBoosting", table_cell_style), Paragraph("0.1236", table_cell_style), Paragraph("0.0260", table_cell_style), Paragraph("0.1612", table_cell_style), Paragraph("0.9994", table_cell_style), Paragraph("3.626 s", table_cell_style), Paragraph("Evaluated", table_cell_style)],
        [Paragraph("Decision Tree Regressor", table_cell_style), Paragraph("0.1266", table_cell_style), Paragraph("0.0248", table_cell_style), Paragraph("0.1574", table_cell_style), Paragraph("0.9995", table_cell_style), Paragraph("0.210 s", table_cell_style), Paragraph("Evaluated", table_cell_style)],
        [Paragraph("Previous-Year Baseline", table_cell_style), Paragraph("0.2037", table_cell_style), Paragraph("0.0550", table_cell_style), Paragraph("0.2346", table_cell_style), Paragraph("0.9988", table_cell_style), Paragraph("< 0.001 s", table_cell_style), Paragraph("Naive Ref.", table_cell_style)]
    ]
    t_bench = Table(bench_data, colWidths=[120, 58, 52, 55, 55, 55, 92])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00296b")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#dcfce7"), colors.HexColor("#ffffff"), colors.HexColor("#f8fafc"), colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Model Selection Rationale:</b><br/>"
        "Ridge Regression achieved the lowest Mean Absolute Error (0.1133 percentile points), representing a <b>44.4% error reduction</b> "
        "compared to the naive previous-year baseline. Historical cutoffs exhibit strong autoregressive persistence with prior-year closing "
        "percentiles, and L2 regularization effectively penalizes collinearity between multi-year lags without tree variance. Ridge also "
        "exhibits the fastest training time (0.12 s) and sub-second inference (27 ms).", body_style
    ))
    story.append(Spacer(1, 10))

    # Diagnostics Plots
    diag_path1 = r"D:\AIML-PROJECT\report\screenshots\actual_vs_predicted.png"
    diag_path2 = r"D:\AIML-PROJECT\report\screenshots\feature_importance.png"
    if os.path.exists(diag_path1) and os.path.exists(diag_path2):
        story.append(Paragraph("<b>Model Diagnostics & Feature Importance</b>", h2_style))
        img_table = Table([
            [Image(diag_path1, width=3.1*inch, height=2.2*inch), Image(diag_path2, width=3.1*inch, height=2.2*inch)]
        ], colWidths=[3.2*inch, 3.2*inch])
        img_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story.append(img_table)
        story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 8. Personalized Recommendation Engine
    # -------------------------------------------------------------
    story.append(Paragraph("6. Personalized Recommendation Engine & Decision Rules", h1_style))
    story.append(Paragraph(
        "The recommendation engine translates continuous predicted cutoffs into actionable candidate advice using an explainable "
        "percentile-gap formulation:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Percentile Gap:</b> &Delta; = P<sub>student</sub> - &ycirc;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Dynamic Margin:</b> M = 1.5 &times; MAE &approx; 0.170 percentile points<br/><br/>"
        "<b>3-Tier Admission Suitability Classification:</b><br/>"
        "• <b>Safer (&Delta; &ge; +M):</b> Candidate percentile comfortably exceeds predicted cutoff with margin buffer.<br/>"
        "• <b>Moderate (-M &le; &Delta; &lt; +M):</b> Candidate is within the competitive boundary (&plusmn;0.17%); viable target choice.<br/>"
        "• <b>Reach (&Delta; &lt; -M):</b> Candidate is below predicted closing cutoff; aspirational reach option.<br/><br/>"
        "Every recommendation transparently presents the historical cutoff progression, intake capacity, and exact gap margin, "
        "avoiding misleading certainty and empowering informed decision-making.", body_style
    ))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 9. Full-Stack Implementation & Deployed System
    # -------------------------------------------------------------
    story.append(Paragraph("7. Full-Stack Implementation & Deployment", h1_style))
    story.append(Paragraph(
        "The architecture is fully decoupled between a modern client-side Single-Page Application and a high-performance REST backend:<br/>"
        "• <b>Frontend Architecture:</b> React 18 SPA built with Vite 5, utilizing functional components, hooks (useState, useEffect), "
        "Lucide-react icons, responsive CSS grid layouts, and deep-link tab synchronization.<br/>"
        "• <b>Backend Architecture:</b> FastAPI asynchronous REST service running via ASGI (Uvicorn), featuring Pydantic schemas, "
        "CORS middleware, and integrated static asset serving.<br/>"
        "• <b>Cloud Deployment:</b> Hosted live on Render Cloud Web Services with continuous Git deployment at "
        "<b>https://mhtcet-college-admission-predictor.onrender.com</b>.", body_style
    ))
    story.append(Spacer(1, 10))

    app_path1 = r"D:\AIML-PROJECT\report\screenshots\app_overview_tab.png"
    app_path2 = r"D:\AIML-PROJECT\report\screenshots\app_recommendations_tab.png"
    if os.path.exists(app_path1) and os.path.exists(app_path2):
        story.append(Paragraph("<b>Deployed Application Interface (Overview & AI Predictor Tabs)</b>", h2_style))
        ui_table = Table([
            [Image(app_path1, width=3.1*inch, height=2.0*inch), Image(app_path2, width=3.1*inch, height=2.0*inch)]
        ], colWidths=[3.2*inch, 3.2*inch])
        ui_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story.append(ui_table)
        story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 10. Verification, Testing & Quality Assurance
    # -------------------------------------------------------------
    story.append(Paragraph("8. Verification, Testing & Quality Assurance", h1_style))
    story.append(Paragraph(
        "A comprehensive automated test suite consisting of 20 unit, integration, and API tests was executed via Pytest, "
        "achieving a <b>100% pass rate (20/20 passed)</b>:", body_style
    ))

    test_data = [
        [Paragraph("Test Suite Module", table_header_style), Paragraph("Tests", table_header_style), Paragraph("Scope of Verification", table_header_style), Paragraph("Result", table_header_style)],
        [Paragraph("test_model_pipeline.py", table_cell_bold), Paragraph("8 tests", table_cell_style), Paragraph("Chronological split, lag features, Ridge fit, inference latency, serialization", table_cell_style), Paragraph("8 / 8 PASS", table_cell_bold)],
        [Paragraph("test_recommendation_engine.py", table_cell_bold), Paragraph("6 tests", table_cell_style), Paragraph("Percentile gap math, Safer/Moderate/Reach bounds, category fallback", table_cell_style), Paragraph("6 / 6 PASS", table_cell_bold)],
        [Paragraph("test_api_endpoints.py", table_cell_bold), Paragraph("6 tests", table_cell_style), Paragraph("FastAPI /api/health, /api/overview, /api/recommend, /api/trends, validation", table_cell_style), Paragraph("6 / 6 PASS", table_cell_bold)],
    ]
    t_test = Table(test_data, colWidths=[130, 45, 240, 72])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00296b")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#dcfce7"), colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 11. Conclusion & Deliverables Summary
    # -------------------------------------------------------------
    story.append(Paragraph("9. Conclusion & Mandatory Deliverables Compliance", h1_style))
    story.append(Paragraph(
        "The project successfully implements an end-to-end, reproducible, AI-driven admission prediction and personalized "
        "recommendation system that eliminates information asymmetry for Maharashtra engineering aspirants. All mandatory "
        "academic syllabus and GitHub repository deliverables are completely fulfilled:", body_style
    ))
    story.append(Paragraph("• <b>Source code / Jupyter notebooks:</b> Clean source under src/, api/, frontend/, tests/, and 6 step-by-step well-commented notebooks in notebooks/.", bullet_style))
    story.append(Paragraph("• <b>README.md:</b> Comprehensive documentation with project overview, live Render link, architecture, and run steps.", bullet_style))
    story.append(Paragraph("• <b>Dataset & Links:</b> Ingested CET Cell documents, normalized cutoffs, seat matrices, and official source links in config/sources.json.", bullet_style))
    story.append(Paragraph("• <b>requirements.txt:</b> Verified dependency file covering all backend, ML, API, test, and document generation tools.", bullet_style))
    story.append(Paragraph("• <b>Saved trained model:</b> Serialized Ridge regression pipeline in models/selected_model.joblib and models/model_metadata.json.", bullet_style))
    story.append(Paragraph("• <b>Screenshots of results & application:</b> Saved high-resolution captures of all 6 React application tabs and diagnostic benchmark plots in report/screenshots/.", bullet_style))
    story.append(Paragraph("• <b>Project report (PDF) & poster photograph:</b> Formal project report in report/final_report.pdf and academic conference poster in report/project_poster.png.", bullet_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Also save a copy to project_report.pdf
    import shutil
    shutil.copyfile(PDF_OUTPUT_1, PDF_OUTPUT_2)
    
    print(f"[OK] Report PDF successfully created:\n  - {PDF_OUTPUT_1}\n  - {PDF_OUTPUT_2}")

if __name__ == "__main__":
    build_pdf_report()

