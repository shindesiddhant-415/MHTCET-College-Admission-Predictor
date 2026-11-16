"""
Script to create the 6 standard Jupyter notebooks with Markdown explanation and code cells.
"""

import json
import os

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.14.3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

def md_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    }

def create_all_notebooks():
    os.makedirs("notebooks", exist_ok=True)
    
    # 01_data_understanding.ipynb
    nb1 = make_notebook([
        md_cell("# 01. Data Understanding & Source Exploration\n**Project**: AI-Based MHT-CET College Admission Prediction & Personalized Recommendation System\n\nThis notebook inspects the official Maharashtra State CET Cell documents, source manifest, and raw extracted text."),
        code_cell("import pandas as pd\nimport json\n\n# Load source manifest\ndf_manifest = pd.read_csv('../docs/source_manifest.csv')\ndf_manifest[['academic_year', 'document_type', 'cap_round', 'file_name', 'status', 'file_size_bytes']]"),
        code_cell("# Inspect interim extracted PDF pages\ndf_pages = pd.read_csv('../dataset/interim/pdf_pages.csv')\nprint(f'Total extracted PDF pages: {len(df_pages)}')\ndf_pages.groupby(['academic_year', 'document_type'])['page_no'].count()")
    ])
    with open("notebooks/01_data_understanding.ipynb", "w") as f:
        json.dump(nb1, f, indent=2)
        
    # 02_eda.ipynb
    nb2 = make_notebook([
        md_cell("# 02. Exploratory Data Analysis (EDA)\nIn this notebook, we analyze the distribution of closing percentiles, year-over-year movements, round progressions, and seat category distributions."),
        code_cell("import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nsns.set_theme(style='whitegrid')\ndf_cut = pd.read_csv('../dataset/processed/cutoffs_long.csv')\ndf_cut.head()"),
        code_cell("# Summary statistics\nprint(df_cut['cutoff_percentile'].describe())"),
        code_cell("# Year-wise and branch-wise mean percentiles\ndf_cut.groupby(['academic_year', 'branch_name'])['cutoff_percentile'].mean().unstack()")
    ])
    with open("notebooks/02_eda.ipynb", "w") as f:
        json.dump(nb2, f, indent=2)

    # 03_data_preprocessing.ipynb
    nb3 = make_notebook([
        md_cell("# 03. Data Preprocessing & Quality Validation\nValidating data integrity, checking missing values, ensuring no zero-imputation of cutoffs, and checking stage codes."),
        code_cell("import pandas as pd\n\ndf_quality = pd.read_csv('../dataset/processed/data_quality_report.csv')\ndf_quality"),
        code_cell("df_cut = pd.read_csv('../dataset/processed/cutoffs_long.csv')\nprint('Missing values per column:\\n', df_cut.isnull().sum())")
    ])
    with open("notebooks/03_data_preprocessing.ipynb", "w") as f:
        json.dump(nb3, f, indent=2)

    # 04_feature_engineering.ipynb
    nb4 = make_notebook([
        md_cell("# 04. Feature Engineering\nConstructing chronological lag features (prev_year_percentile, prev2_year_percentile, percentile_trend, prev_year_merit_no, seat capacity) without target leakage."),
        code_cell("import pandas as pd\n\ndf_model = pd.read_csv('../dataset/model/model_dataset.csv')\nprint(f'Model-ready records: {len(df_model)}')\ndf_model[['academic_year', 'institute_name', 'branch_name', 'cutoff_percentile', 'prev_year_percentile', 'percentile_trend']].head(10)")
    ])
    with open("notebooks/04_feature_engineering.ipynb", "w") as f:
        json.dump(nb4, f, indent=2)

    # 05_model_experiments.ipynb
    nb5 = make_notebook([
        md_cell("# 05. Model Experiments & Comparative Evaluation\nComparing Baseline, Ridge Regression, Decision Tree Regressor, Random Forest, and HistGradientBoosting using expanding chronological splits."),
        code_cell("import pandas as pd\n\ndf_comp = pd.read_csv('../results/model_comparison.csv')\ndf_comp"),
        code_cell("with open('../results/test_metrics.json') as f:\n    import json\n    best = json.load(f)\nprint('Best Model Summary:', best)")
    ])
    with open("notebooks/05_model_experiments.ipynb", "w") as f:
        json.dump(nb5, f, indent=2)

    # 06_model_analysis.ipynb
    nb6 = make_notebook([
        md_cell("# 06. Model Diagnostics, Error Analysis & Explainability\nAnalyzing residuals, error by branch and CAP round, feature importances, and failure modes."),
        code_cell("from PIL import Image\nimport os\n\n# Display generated diagnostic plots\nImage.open('../results/actual_vs_predicted.png')"),
        code_cell("Image.open('../results/error_distribution.png')"),
        code_cell("Image.open('../results/feature_importance.png')")
    ])
    with open("notebooks/06_model_analysis.ipynb", "w") as f:
        json.dump(nb6, f, indent=2)

    print("All 6 Jupyter notebooks generated successfully.")

if __name__ == "__main__":
    create_all_notebooks()

