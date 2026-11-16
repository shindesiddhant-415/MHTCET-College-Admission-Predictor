# Data Dictionary

This document provides complete field definitions, data types, and allowed values for all datasets used in the **AI-Based MHT-CET College Admission Prediction and Personalized Recommendation System**.

---

## 1. Normalized Cutoff Dataset (`dataset/processed/cutoffs_long.csv`)

| Column Name | Data Type | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `academic_year` | String | `"2026-27"` | Academic year of CAP admission cycle (2023-24, 2024-25, 2025-26, 2026-27). |
| `year_num` | Integer | `2026` | Numeric integer year index for chronological modeling. |
| `cap_round` | Integer | `1` | Centralized Admission Process round (1, 2, 3, or 4). |
| `seat_type` | String | `"MH"` | Document seat category pool (MH = Maharashtra State Candidate seats). |
| `institute_code`| String | `"06006"` | Official 5-digit Directorate of Technical Education (DTE) institute code. |
| `institute_name`| String | `"COEP Technological University, Pune"` | Official name of the engineering college. |
| `institute_status` | String | `"Government Autonomous"` | Institutional status (Government, Autonomous, Aided, Un-Aided, Minority). |
| `course_code` | String | `"0600624510"` | Official 10-digit DTE course code (Institute code + 3-digit branch + shift + status). |
| `branch_name` | String | `"Computer Engineering"` | Name of engineering discipline/course. |
| `seat_pool` | String | `"State Level"` | Seat reservation pool (State Level, Home University - HU, Other than Home University - OHU). |
| `seat_category_code` | String | `"GOPENS"` | Official reservation category code (GOPENS, LOPENS, GOBCS, LOBCS, GSCS, GSTS, EWS, TFWS, etc.). |
| `stage_code` | String | `"I"` | CAP allotment stage printed in official document (Stage I). |
| `merit_no` | Integer | `1494` | General state merit number of the closing candidate. |
| `cutoff_percentile` | Float | `98.941828` | Exact MHT-CET closing percentile (0.0000000 to 100.0000000). Target variable. |
| `source_file` | String | `"2026ENGG_CAP1_MH_CutOff_V1.pdf"` | Source official PDF file name. |
| `source_page` | Integer | `1` | Page number within the source document where this record is found. |

---

## 2. Seat Matrix Dataset (`dataset/processed/seat_matrix.csv`)

| Column Name | Data Type | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `academic_year` | String | `"2026-27"` | Academic admission year. |
| `institute_code`| String | `"06006"` | 5-digit institute identifier. |
| `institute_name`| String | `"COEP Technological University, Pune"` | College name. |
| `course_code` | String | `"0600624510"` | 10-digit course identifier. |
| `branch_name` | String | `"Computer Engineering"` | Branch name. |
| `institute_status` | String | `"Government Autonomous"` | Institutional category. |
| `total_intake` | Integer | `120` | Total approved sanctioned intake for the branch. |
| `state_seats` | Integer | `102` | Seats allocated for Maharashtra State (CAP) pool. |
| `minority_seats`| Integer | `0` | Seats reserved for linguistic/religious minority quotas. |
| `all_india_seats`| Integer | `18` | Seats allocated under All India JEE Main merit. |
| `institute_seats`| Integer | `0` | Institutional / Management quota seats. |
| `orphan_seats` | Integer | `1` | Supernumerary seats reserved for orphan candidates. |
| `source_file` | String | `"2026_fe_seatmatrix_V1.pdf"` | Seat matrix source document. |
| `source_page` | Integer | `1` | Page number in the seat matrix PDF. |

---

## 3. Machine Learning Dataset (`dataset/model/model_dataset.csv`)

| Column Name | Feature Type | Description |
| :--- | :--- | :--- |
| `cutoff_percentile` | Target ($y$) | Closing cutoff percentile for the target academic year. |
| `prev_year_percentile` | Numeric ($t-1$) | Exact cutoff percentile for the same college, branch, round, and category in year $t-1$. |
| `prev2_year_percentile` | Numeric ($t-2$) | Cutoff percentile for the same combination two years prior ($t-2$). |
| `percentile_trend` | Numeric | $\text{prev\_year\_percentile} - \text{prev2\_year\_percentile}$ (short-term momentum). |
| `prev_year_merit_no` | Numeric ($t-1$) | General state merit number in previous year. |
| `prev_year_intake` | Numeric ($t-1$) | Sanctioned student capacity in previous year. |
| `intake_change` | Numeric | Shift in intake capacity ($\text{intake}_{t-1} - \text{intake}_{t-2}$). |
| `institute_code` | Categorical | College identifier (One-Hot Encoded). |
| `course_code` | Categorical | Specific branch offering identifier (One-Hot Encoded). |
| `branch_name` | Categorical | Engineering discipline (One-Hot Encoded). |
| `cap_round` | Categorical | Admission round 1, 2, 3, or 4 (One-Hot Encoded). |
| `seat_pool` | Categorical | State Level / Home University / Other than Home University (One-Hot Encoded). |
| `seat_category_code` | Categorical | Reservation quota (One-Hot Encoded). |
| `stage_code` | Categorical | Stage code (One-Hot Encoded). |

