"""
Streamlit Page 3: Model Performance & Comparative Evaluation
"""

import os
import json
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Model Performance", page_icon="🔬", layout="wide")

st.title("🔬 Machine Learning Model Evaluation & Benchmarks")
st.write("Rigorous comparative evaluation of regression models on chronologically held-out test data (Year 2026-27).")

# Load model comparison
try:
    df_comp = pd.read_csv("results/model_comparison.csv")
    with open("models/model_metadata.json", "r") as f:
        meta = json.load(f)
        
    st.subheader("1. Regression Models Benchmark Leaderboard")
    st.dataframe(
        df_comp.style.highlight_min(subset=["MAE", "RMSE", "MSE"], color="#d4edda")
                     .highlight_max(subset=["R2"], color="#d4edda")
                     .format({"MAE": "{:.4f}", "MSE": "{:.4f}", "RMSE": "{:.4f}", "R2": "{:.4f}"}),
        use_container_width=True,
        hide_index=True
    )
    
    st.info(f"🏆 **Selected Production Model**: **{meta['best_model_name']}** achieves the lowest Mean Absolute Error of **{meta['validation_mae']:.4f}** percentile points and $R^2 = {meta['validation_r2']:.4f}$ on completely unseen test data.")
    
    st.divider()
    
    st.subheader("2. Evaluation Plots & Residual Diagnostics")
    
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("results/actual_vs_predicted.png"):
            st.image(Image.open("results/actual_vs_predicted.png"), caption="Actual vs Predicted Cutoff Percentiles", use_container_width=True)
    with col2:
        if os.path.exists("results/error_distribution.png"):
            st.image(Image.open("results/error_distribution.png"), caption="Residual / Error Distribution (Centered at 0)", use_container_width=True)
            
    st.write("")
    
    col3, col4 = st.columns(2)
    with col3:
        if os.path.exists("results/model_comparison_bar.png"):
            st.image(Image.open("results/model_comparison_bar.png"), caption="Model Comparison by MAE (Lower is Better)", use_container_width=True)
    with col4:
        if os.path.exists("results/feature_importance.png"):
            st.image(Image.open("results/feature_importance.png"), caption="Top Feature Weights / Importances", use_container_width=True)
            
    st.divider()
    
    st.subheader("3. Critical Analysis & Viva Discussion Points")
    st.markdown("""
    - **Why Chronological Splitting?** Standard random $k$-fold cross-validation allows future cutoff information to leak into training. In this system, records from 2024 were used for initial training, 2025 for validation, and 2026 exclusively for testing, mirroring real-world future admission cycles.
    - **Why Did Ridge Regression Perform Best?** Cutoff percentiles across successive years exhibit strong linear autoregressive trends ($\text{prev\_year\_percentile}$ has the highest predictive weight). $L_2$ regularization effectively damped high-cardinality institute-course dummy variables without overfitting.
    - **Handling Class Imbalance & Edge Cases**: Regression algorithms do not use SMOTE. Categories with sparse representation (e.g. ST, Defense) have wider variance, which is transparently reflected in the suitability error margin ($M = 1.5 \times \text{MAE}$).
    """)

except Exception as e:
    st.error(f"Error loading evaluation results: {e}")
