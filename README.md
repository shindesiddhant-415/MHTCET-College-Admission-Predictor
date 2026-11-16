# 🎓 AI-Based MHT-CET College Admission Prediction & Personalized Recommendation System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Tests Passing](https://img.shields.io/badge/tests-13%20passed-brightgreen.svg)]()

An advanced, end-to-end Machine Learning decision-support system for candidates participating in the **Maharashtra State Centralized Admission Process (CAP)** for undergraduate engineering admissions.

Developed for **Practical No. 07: Mini Project**, Third Year B.Tech (Artificial Intelligence and Machine Learning Lab - Course Code: 2311331L), MIT Academy of Engineering (MITAOE), Pune.

---

## 🌟 Key Capabilities

- **Official PDF Ingestion**: Extracts, parses, and normalizes 18 official Maharashtra State CET Cell documents across 4 academic years (2023–24 to 2026–27) covering 22+ top engineering institutes and 8 branches.
- **Leakage-Free Feature Engineering**: Constructs chronological lag features ($t-1$, $t-2$), cutoff trends, merit indices, and seat intake shifts without future target leakage.
- **Rigorous Model Benchmarking**: Compares 5 algorithms using strict chronological splitting (Train: 2024, Val: 2025, Test: 2026):
  1. *Previous-Year Cutoff Baseline*
  2. *Ridge Regression (L2 / SGD Regularized Linear Model)*
  3. *Decision Tree Regressor*
  4. *Random Forest Regressor (Ensemble Bagging)*
  5. *HistGradientBoosting Regressor (Ensemble Boosting)*
- **Personalized Recommendation Engine**: Calculates the percentile gap between the candidate's score and estimated cutoff, grouping choices into **Safer**, **Moderate**, and **Reach** options using validation error margins ($M = 1.5 \times \text{MAE}$).
- **Interactive Streamlit Web Dashboard**: 5-page dashboard featuring live recommendations, historical cutoff trends, college comparisons, and diagnostic model evaluations.
- **Comprehensive Automated Test Suite**: 13 unit tests validating schemas, ranges, edge cases, and test cases TC-1 through TC-5.

---

## 📊 Model Evaluation Summary (Held-Out Test Year 2026-27)

| Rank | Model | MAE (percentile pts) ↓ | RMSE ↓ | $R^2$ Score ↑ | Training Time (s) | Inference Time (s) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **Ridge Regression (SGD/L2)** | **0.1133** | **0.1415** | **0.9996** | 0.120 s | 0.027 s |
| 🥈 | **Random Forest Regressor** | 0.1168 | 0.1442 | 0.9996 | 1.296 s | 0.082 s |
| 🥉 | **HistGradientBoosting Regressor** | 0.1236 | 0.1612 | 0.9994 | 3.626 s | 0.051 s |
| 4 | **Decision Tree Regressor** | 0.1266 | 0.1574 | 0.9995 | 0.210 s | 0.030 s |
| 5 | **Previous-Year Baseline** | 0.2037 | 0.2346 | 0.9988 | < 0.001 s | < 0.001 s |

*All trained ML models significantly outperform the naive previous-year baseline.*

---

## 📁 Repository Structure

```text
MHTCET-College-Recommender/
├── app/                              # Streamlit web application
│   ├── app.py                        # Landing page & dashboard
│   ├── pages/
│   │   ├── 1_🎯_Recommendations.py   # Personalized predictor & shortlisting
│   │   ├── 2_📈_Cutoff_Trends.py      # Historical trends & CAP round drops
│   │   ├── 3_🔬_Model_Performance.py  # Model leaderboard & diagnostic plots
│   │   ├── 4_⚖️_College_Comparison.py # Head-to-head college comparison
│   │   └── 5_📚_Dataset_Information.py# Audit trail, manifest & ethics
│   └── utils/
│       ├── input_validation.py       # Input validation helpers
│       └── display_helpers.py        # Badge formatting & UI helpers
├── config/
│   └── sources.json                  # Source URLs, document IDs & metadata
├── dataset/
│   ├── raw/pdfs/                     # Official CAP cutoff & seat matrix PDFs
│   ├── interim/pdf_pages.csv         # Raw extracted text per PDF page
│   ├── processed/
│   │   ├── cutoffs_long.csv          # Normalized long-format cutoffs (32k+ rows)
│   │   ├── seat_matrix.csv           # Sanctioned seat matrix records
│   │   └── data_quality_report.csv   # Data audit & validation report
│   └── model/
│       └── model_dataset.csv         # ML-ready dataset with engineered lag features
├── docs/
│   ├── data_dictionary.md            # Comprehensive schema definitions
│   ├── architecture.md               # End-to-end architecture diagram & notes
│   └── source_manifest.csv           # Traceability manifest for all 18 documents
├── models/
│   ├── selected_model.joblib         # Refitted production model
│   └── model_metadata.json           # Model configuration, MAE & margins
├── notebooks/
│   ├── 01_data_understanding.ipynb   # Data inspection notebook
│   ├── 02_eda.ipynb                  # Exploratory Data Analysis
│   ├── 03_data_preprocessing.ipynb   # Data cleaning & validation
│   ├── 04_feature_engineering.ipynb  # Chronological lag construction
│   ├── 05_model_experiments.ipynb    # Algorithm benchmarking
│   └── 06_model_analysis.ipynb       # Diagnostic error analysis
├── report/
│   ├── final_report.docx             # Complete project report in required template
│   └── screenshots/                  # High-resolution evaluation & EDA figures
├── results/                          # Benchmark tables & saved plots
├── src/
│   ├── data/                         # Data extraction & parsing scripts
│   ├── features/                     # Feature engineering scripts
│   ├── models/                       # Training, evaluation & inference scripts
│   └── recommendations/              # Personalized recommendation engine
├── tests/                            # Automated test suite (TC-1 to TC-5)
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and set up a virtual environment:
```powershell
git clone https://github.com/your-username/MHTCET-College-Recommender.git
cd MHTCET-College-Recommender
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Data & ML Pipeline (Reproducibility)
Run the pipeline modules in sequence:
```powershell
# 1. Download/verify official source PDFs
python src/data/download_pdfs.py

# 2. Extract text page-by-page using PyMuPDF
python src/data/extract_pdf_text.py

# 3. Parse tables into normalized CSV
python src/data/parse_cutoff_tables.py
python src/data/parse_seat_matrix.py

# 4. Perform data quality checks
python src/data/validate_data.py

# 5. Build chronological lag features
python src/features/build_features.py

# 6. Train and evaluate all regression algorithms
python src/models/train_models.py

# 7. Generate diagnostic plots and EDA
python src/models/explain_model.py
python src/features/generate_eda_plots.py
```

### 3. Run Automated Tests
```powershell
python -m pytest tests -v
```

### 4. Launch Streamlit Web Application
```powershell
streamlit run app/app.py
```

---

## 🧪 Deployment Test Cases (TC-1 to TC-5)

| Test Case | Description | Input | Expected Output | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TC-1** | Valid Prediction | 92.50%, GOPENS, State Level | Displays predicted cutoff and option list | ✅ Pass |
| **TC-2** | Out-of-Bounds Percentile | Percentile = -5.0 or 105.0 | Rejected with clear input validation error | ✅ Pass |
| **TC-3** | Unseen Category | Non-existent category code | Returns clean error status without crash | ✅ Pass |
| **TC-4** | New Institute / Branch | Institute code 99999 | Returns "Insufficient historical data" | ✅ Pass |
| **TC-5** | Empty Filters | Non-matching branch/city | Displays clean no-results message | ✅ Pass |

---

## ⚖️ Ethical Guidelines & Responsible AI

- **Transparency & Explainability**: Recommendations explicitly disclose historical cutoff trends, model validation MAE, and the percentile gap reason for every placement.
- **Category Fairness**: The system enforces official reservation categories (OBC, SC, ST, EWS, TFWS) as selected by the user without making unsolicited assumptions.
- **Privacy by Design**: No personal identity documents, roll numbers, or personal identifying information are collected or stored.
- **Decision-Support Notice**: This tool is an academic decision aid and does not guarantee admission. Final allotments are governed solely by Maharashtra State CET Cell official procedures.
