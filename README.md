# 🎓 AI-Based MHT-CET College Admission Prediction & Personalized Recommendation System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/frontend-React%2018%20(Vite)-61dafb.svg)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Tests Passing](https://img.shields.io/badge/tests-20%20passed-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced, full-stack Machine Learning decision-support platform for candidates participating in the **Maharashtra State Centralized Admission Process (CAP)** for undergraduate engineering admissions.

Built with a **Modern React 18 Single-Page Application (Vite)** frontend powered by a high-performance **FastAPI REST ML Service** backend.

Developed for **Practical No. 07: Mini Project**, Third Year B.Tech (Artificial Intelligence and Machine Learning Lab - Course Code: `2311331L`), MIT Academy of Engineering (MITAOE), Pune.

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
- **Modern React 18 Frontend**: Responsive SPA with dynamic sliders, branch/region chips, interactive shortlists, visual badges, and one-click CSV export.
- **FastAPI REST API**: High-performance backend providing endpoints for predictions, multi-year trends, college comparison matrices, and diagnostics.
- **Automated Test Suite**: 20 unit tests validating schemas, ranges, API endpoints, and deployment test cases TC-1 through TC-5 (100% pass rate).

---

## 📊 Model Evaluation Summary (Held-Out Test Year 2026-27)

| Rank | Model | MAE (percentile pts) ↓ | MSE ↓ | RMSE ↓ | $R^2$ Score ↑ | Training Time (s) | Inference Time (s) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **Ridge Regression (SGD/L2)** | **0.1133** | **0.0200** | **0.1415** | **0.9996** | 0.120 s | 0.027 s |
| 🥈 | **Random Forest Regressor** | 0.1168 | 0.0208 | 0.1442 | 0.9996 | 1.296 s | 0.082 s |
| 🥉 | **HistGradientBoosting Regressor** | 0.1236 | 0.0260 | 0.1612 | 0.9994 | 3.626 s | 0.051 s |
| 4 | **Decision Tree Regressor** | 0.1266 | 0.0248 | 0.1574 | 0.9995 | 0.210 s | 0.030 s |
| 5 | **Previous-Year Baseline** | 0.2037 | 0.0550 | 0.2346 | 0.9988 | < 0.001 s | < 0.001 s |

---

## 📁 Repository Structure

```text
MHTCET-College-Recommender/
├── api/                              # FastAPI REST ML Backend
│   └── main.py                       # REST API endpoints & static React serving
├── frontend/                         # Modern React 18 Single-Page Application (Vite)
│   ├── index.html                    # HTML root template
│   ├── package.json                  # Dependencies: react, lucide-react, vite
│   ├── vite.config.js                # Vite build config & proxy to FastAPI
│   └── src/
│       ├── App.jsx                   # Main layout & tab state manager
│       ├── main.jsx                  # React DOM root mounting
│       ├── index.css                 # Clean academic CSS design system
│       ├── components/
│       │   ├── Navbar.jsx            # Top navigation bar
│       │   ├── OverviewTab.jsx       # Dashboard KPIs & project summary
│       │   ├── RecommendationsTab.jsx# Candidate form, option list & CSV export
│       │   ├── CutoffTrendsTab.jsx   # Multi-year cutoff trends & round drops
│       │   ├── ModelPerformanceTab.jsx# Benchmarking leaderboard & diagnostic plots
│       │   ├── CollegeComparisonTab.jsx# Head-to-head college & intake comparison
│       │   └── DatasetInfoTab.jsx    # Manifest, quality report & category guide
│       └── services/
│           └── api.js                # Frontend API fetch services
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
│   ├── selected_model.joblib         # Refitted production Ridge pipeline
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
│   ├── final_report_summary.md       # Markdown report with all sections & tables
│   └── screenshots/                  # High-resolution evaluation & EDA figures
├── results/                          # Benchmark tables & saved plots
├── src/
│   ├── data/                         # Data extraction & parsing scripts
│   ├── features/                     # Feature engineering scripts
│   ├── models/                       # Training, evaluation & inference scripts
│   └── recommendations/              # Personalized recommendation engine
├── tests/                            # Automated test suite (20 / 20 passed)
│   ├── test_api.py                   # FastAPI REST endpoint tests
│   ├── test_data_validation.py       # Dataset schemas, ranges & null checks
│   ├── test_prediction.py            # TC-1 to TC-4 test cases
│   └── test_recommendations.py       # TC-5, grouping & sorting checks
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install dependencies:
```powershell
git clone https://github.com/your-username/MHTCET-College-Recommender.git
cd MHTCET-College-Recommender

# Install Python backend dependencies
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Install React frontend dependencies
cd frontend
pnpm install
cd ..
```

### 2. Run Data & ML Pipeline (Reproducibility)
```powershell
python src/data/download_pdfs.py
python src/data/extract_pdf_text.py
python src/data/parse_cutoff_tables.py
python src/data/parse_seat_matrix.py
python src/data/validate_data.py
python src/features/build_features.py
python src/models/train_models.py
python src/models/explain_model.py
python src/features/generate_eda_plots.py
```

### 3. Run Automated Tests (20 Tests)
```powershell
$env:PYTHONPATH="."
python -m pytest tests -v
```

### 4. Launch Application (React Frontend + FastAPI Backend)

#### Option A: Run Full Application from FastAPI (Single Command)
First build the React frontend:
```powershell
cd frontend
pnpm run build
cd ..
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```
*Open [http://localhost:8000](http://localhost:8000) in your browser.*

#### Option B: Run in Development Mode with Hot Reload
**Terminal 1 (FastAPI Backend):**
```powershell
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```
**Terminal 2 (React Vite Dev Server):**
```powershell
cd frontend
pnpm run dev
```
*Open [http://localhost:5173](http://localhost:5173) in your browser.*

---

## 🧪 Deployment Test Cases (TC-1 to TC-5)

| Test Case | Description | Input | Expected Output | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TC-1** | Valid Prediction | 92.50%, GOPENS, State Level | Displays predicted cutoff and option list in React UI | ✅ Pass |
| **TC-2** | Out-of-Bounds Percentile | Percentile = -5.0 or 105.0 | Rejected with clear input validation error | ✅ Pass |
| **TC-3** | Unseen Category | Non-existent category code | Returns clean error status without crash | ✅ Pass |
| **TC-4** | New Institute / Branch | Institute code 99999 | Returns "Insufficient historical data" | ✅ Pass |
| **TC-5** | Empty Filters | Non-matching branch/city | Displays clean no-results message | ✅ Pass |

---

## ⚖️ Ethical Guidelines & Responsible AI

- **Transparency & Explainability**: Recommendations explicitly disclose historical cutoff trends, model validation MAE, and the percentile gap reason for every placement.
- **Category Fairness**: The system enforces official reservation categories (`GOPENS`, `GOBCS`, `GSCS`, `GSTS`, `EWS`, `TFWS`) as selected by the user without making unsolicited assumptions.
- **Privacy by Design**: No personal identity documents, roll numbers, or personal identifying information are collected or stored.
- **Decision-Support Notice**: This tool is an academic decision aid and does not guarantee admission. Final allotments are governed solely by Maharashtra State CET Cell official procedures.
