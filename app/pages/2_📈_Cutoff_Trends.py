"""
Streamlit Page 2: Cutoff Trends Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cutoff Trends", page_icon="📈", layout="wide")

st.title("📈 Historical Cutoff Trends & Analytics")
st.write("Analyze cutoff percentile movements across academic years, CAP admission rounds, and seat categories.")

@st.cache_data
def get_cutoffs():
    return pd.read_csv("dataset/processed/cutoffs_long.csv")

df = get_cutoffs()

col1, col2, col3 = st.columns(3)
with col1:
    selected_colleges = st.multiselect(
        "Select Institutes for Trend Analysis",
        options=sorted(df["institute_name"].unique()),
        default=[
            "COEP Technological University, Pune",
            "Veermata Jijabai Technological Institute (VJTI), Mumbai",
            "Pune Institute of Computer Technology (PICT), Pune"
        ]
    )
with col2:
    selected_branches = st.multiselect(
        "Select Branch",
        options=sorted(df["branch_name"].unique()),
        default=["Computer Engineering", "Information Technology"]
    )
with col3:
    selected_category = st.selectbox(
        "Select Seat Category",
        options=sorted(df["seat_category_code"].unique()),
        index=0
    )

filtered_df = df[
    (df["institute_name"].isin(selected_colleges)) &
    (df["branch_name"].isin(selected_branches)) &
    (df["seat_category_code"] == selected_category)
]

if filtered_df.empty:
    st.warning("No records found for the selected combinations.")
else:
    st.subheader("1. Year-over-Year Cutoff Trajectory (CAP Round I)")
    round1_df = filtered_df[filtered_df["cap_round"] == 1]
    
    fig_trend = px.line(
        round1_df,
        x="academic_year",
        y="cutoff_percentile",
        color="institute_name",
        line_dash="branch_name",
        markers=True,
        title=f"Cutoff Movement across Academic Years ({selected_category} - Round 1)",
        labels={"academic_year": "Academic Year", "cutoff_percentile": "Closing Percentile", "institute_name": "College"},
        template="plotly_white"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.divider()
    
    st.subheader("2. Round-wise Cutoff Progression (Drop from Round 1 to Round 4)")
    st.write("Demonstrates how cutoff percentiles typically relax across successive CAP rounds.")
    
    fig_rounds = px.box(
        filtered_df,
        x="cap_round",
        y="cutoff_percentile",
        color="institute_name",
        points="all",
        title="Cutoff Percentile Distribution by CAP Round",
        labels={"cap_round": "CAP Admission Round", "cutoff_percentile": "Percentile", "institute_name": "College"}
    )
    st.plotly_chart(fig_rounds, use_container_width=True)
