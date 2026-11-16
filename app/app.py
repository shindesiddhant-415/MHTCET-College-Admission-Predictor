"""
Streamlit Main Application: Home / Dashboard
Project: AI-Based MHT-CET College Admission Prediction and Personalized Recommendation System
"""

import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="MHT-CET Admission Predictor & Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished academic UI
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #0d3b66;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        color: #555555;
        margin-bottom: 25px;
    }
    .kpi-card {
        background-color: #f8f9fa;
        border-left: 5px solid #00509d;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    .kpi-num {
        font-size: 26px;
        font-weight: bold;
        color: #00296b;
    }
    .kpi-lbl {
        font-size: 13px;
        color: #666666;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 AI-Based MHT-CET College Admission Prediction & Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Decision-Support System for Maharashtra Engineering Centralized Admission Process (CAP) | Practical No. 07 Mini-Project</div>', unsafe_allow_html=True)

# Load data summaries
@st.cache_data
def load_overview_data():
    cutoffs = pd.read_csv("dataset/processed/cutoffs_long.csv")
    seat_matrix = pd.read_csv("dataset/processed/seat_matrix.csv")
    with open("models/model_metadata.json", "r") as f:
        meta = json.load(f)
    return cutoffs, seat_matrix, meta

try:
    df_cut, df_sm, meta = load_overview_data()
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-num">{len(df_cut):,}</div>
            <div class="kpi-lbl">Normalized CAP Records</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-num">{df_cut['institute_code'].nunique()}</div>
            <div class="kpi-lbl">Colleges Tracked</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-num">{meta['validation_mae']:.4f}</div>
            <div class="kpi-lbl">Best Model MAE ({meta['best_model_name'][:12]})</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-num">{meta['forecast_year']}</div>
            <div class="kpi-lbl">Target Admission Cycle</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.write("")

    # Two column overview
    left_col, right_col = st.columns([3, 2])
    
    with left_col:
        st.subheader("📌 Project Motivation & Objectives")
        st.write("""
        Students seeking admission through the Maharashtra State CET Cell CAP face high uncertainty when shortlisting 
        colleges and branches. Cutoffs fluctuate yearly across multiple rounds, categories (GOPENS, TFWS, EWS, OBC, SC, ST), 
        and seat pools.
        
        This system:
        - **Structures Official Records**: Normalizes 4 academic years (2023-24 to 2026-27) across 14 CAP rounds and seat matrices.
        - **Machine Learning Forecasting**: Compares 5 algorithms (Baseline, Ridge Regression, Decision Tree, Random Forest, HistGradientBoosting) with expanding chronological evaluation.
        - **Personalized Decision Support**: Generates custom recommendations grouped into **Safer**, **Moderate**, and **Reach** options based on the student's exact percentile and official category.
        """)
        
        st.info("ℹ️ **Academic & Ethical Disclaimer**: This platform is an educational decision-support tool built for research and evaluation. It cannot guarantee admission outcomes, which depend on final official CET Cell CAP allotments.")

    with right_col:
        st.subheader("⚡ Quick Navigation")
        st.markdown("""
        Use the sidebar to explore the modules:
        - 🎯 **[Personalized Recommendations](Recommendations)**: Enter your MHT-CET percentile and get ranked college options.
        - 📈 **[Cutoff Trends](Cutoff_Trends)**: Inspect historical percentile movement and round progressions.
        - 🔬 **[Model Performance](Model_Performance)**: Review the regression benchmarks, error analysis, and feature importances.
        - ⚖️ **[College Comparison](College_Comparison)**: Compare two or more engineering institutes side-by-side.
        - 📚 **[Dataset Information](Dataset_Information)**: View official sources, data dictionary, and data quality metrics.
        """)
        
    st.divider()
    
    # High-level data overview charts
    st.subheader("📊 Dataset Overview at a Glance")
    c1, c2 = st.columns(2)
    with c1:
        fig_yr = px.bar(
            df_cut["academic_year"].value_counts().reset_index(),
            x="academic_year",
            y="count",
            labels={"academic_year": "Academic Year", "count": "Parsed Cutoff Records"},
            title="Records by Academic Year",
            color_discrete_sequence=["#1f77b4"]
        )
        st.plotly_chart(fig_yr, use_container_width=True)
    with c2:
        fig_br = px.bar(
            df_cut["branch_name"].value_counts().reset_index(),
            y="branch_name",
            x="count",
            orientation="h",
            labels={"branch_name": "Branch", "count": "Records"},
            title="Records by Engineering Discipline",
            color_discrete_sequence=["#2ca02c"]
        )
        st.plotly_chart(fig_br, use_container_width=True)

except Exception as e:
    st.error(f"Error loading system assets: {e}")
