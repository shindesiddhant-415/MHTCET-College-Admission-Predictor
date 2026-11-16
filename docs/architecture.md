# System Architecture

The **AI-Based MHT-CET College Admission Prediction and Personalized Recommendation System** is built on an end-to-end reproducible machine learning pipeline.

---

## 1. Architectural Block Diagram

```mermaid
flowchart TD
    subgraph Data_Pipeline [Data Collection & Normalization]
        A[Official CET Cell Cutoff & Seat Matrix PDFs] --> B[PyMuPDF Page-by-Page Text Extraction]
        B --> C[Regex Table Parser & Normalizer]
        C --> D[Data Quality & Integrity Validation]
        D --> E[(Normalized Cutoffs & Seat Matrix CSV)]
    end

    subgraph Feature_Store [Feature Engineering]
        E --> F[Chronological Lag Feature Builder]
        F --> G[Prior-Year Cutoffs t-1 & t-2]
        F --> H[Cutoff Momentum Trend & Intake Shifts]
        G --> I[(Model Dataset)]
        H --> I
    end

    subgraph ML_Benchmarking [Model Training & Evaluation]
        I --> J[Chronological Split: Train 2024 / Val 2025 / Test 2026]
        J --> K1[Previous-Year Baseline]
        J --> K2[Ridge Regression - SGD/L2]
        J --> K3[Decision Tree Regressor]
        J --> K4[Random Forest Regressor]
        J --> K5[HistGradientBoosting Regressor]
        K1 & K2 & K3 & K4 & K5 --> L[Model Evaluation: MAE, RMSE, R²]
        L --> M[Model Selection & Production Refit]
        M --> N[(Saved Pipeline & Metadata)]
    end

    subgraph Decision_Engine [Recommendation & Deployment]
        N --> O[Personalized Recommendation Engine]
        P[Student Inputs: Percentile, Category, Branch, Region] --> O
        O --> Q[Percentile Gap Calculation]
        Q --> R[Suitability Grouping: Safer / Moderate / Reach]
        R --> S[Streamlit Multi-Page Web Dashboard]
    end
```

---

## 2. Chronological Splitting Methodology

Unlike standard randomized splits that cause temporal look-ahead leakage, this system adopts an expanding chronological window:

- **2023–24 (`year_num = 2023`)**: Base historical year used purely to compute initial lag features.
- **2024–25 (`year_num = 2024`)**: Initial training target set ($N = 6,888$).
- **2025–26 (`year_num = 2025`)**: Validation target set ($N = 6,888$) for hyperparameter tuning.
- **2026–27 (`year_num = 2026`)**: Held-out final test set ($N = 9,184$) for model comparison and reporting.
- **2027–28 Forecast**: Final production model refitted on all historical targets ($N = 22,960$) to generate future predictions.

---

## 3. Recommendation Grouping Logic

For every candidate offering $i$:

$$\text{Gap}_i = \text{Percentile}_{\text{Student}} - \hat{y}_i$$

Where $\hat{y}_i$ is the ML predicted closing percentile. Using the validation error margin $M = 1.5 \times \text{MAE}_{\text{val}}$:

- **Safer**: $\text{Gap}_i > M$ (Comfortable admission buffer)
- **Moderate**: $-M \le \text{Gap}_i \le M$ (Competitive margin)
- **Reach**: $\text{Gap}_i < -M$ (Ambitious / Dream option)
