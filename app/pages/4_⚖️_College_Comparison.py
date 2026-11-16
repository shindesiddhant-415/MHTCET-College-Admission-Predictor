"""
Streamlit Page 4: College Comparison
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="College Comparison", page_icon="⚖️", layout="wide")

st.title("⚖️ Head-to-Head College & Branch Comparison")
st.write("Compare historical cutoffs, estimated future closing scores, and total seat capacities across multiple institutes.")

@st.cache_data
def load_comp_data():
    cutoffs = pd.read_csv("dataset/processed/cutoffs_long.csv")
    seat_matrix = pd.read_csv("dataset/processed/seat_matrix.csv")
    return cutoffs, seat_matrix

df_cut, df_sm = load_comp_data()

all_colleges = sorted(df_cut["institute_name"].unique())
colleges_selected = st.multiselect(
    "Select 2 or More Colleges to Compare",
    options=all_colleges,
    default=all_colleges[:2] if len(all_colleges) >= 2 else all_colleges
)

branch_selected = st.selectbox(
    "Select Discipline / Branch",
    options=sorted(df_cut["branch_name"].unique()),
    index=0
)

category_selected = st.selectbox(
    "Select Seat Category",
    options=sorted(df_cut["seat_category_code"].unique()),
    index=0
)

if len(colleges_selected) < 2:
    st.info("Please select at least 2 institutes to compare side-by-side.")
else:
    comp_df = df_cut[
        (df_cut["institute_name"].isin(colleges_selected)) &
        (df_cut["branch_name"] == branch_selected) &
        (df_cut["seat_category_code"] == category_selected) &
        (df_cut["cap_round"] == 1)
    ]
    
    if comp_df.empty:
        st.warning("No comparable records found for the chosen filters.")
    else:
        st.subheader(f"📊 Cutoff Percentile Comparison: {branch_selected} ({category_selected} - CAP Round 1)")
        fig_bar = px.bar(
            comp_df,
            x="academic_year",
            y="cutoff_percentile",
            color="institute_name",
            barmode="group",
            text_auto=".2f",
            title=f"Closing Percentile Comparison Across Years",
            labels={"academic_year": "Academic Year", "cutoff_percentile": "Cutoff Percentile", "institute_name": "College"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        
        st.subheader("💺 Seat Matrix & Intake Comparison")
        sm_filtered = df_sm[
            (df_sm["institute_name"].isin(colleges_selected)) &
            (df_sm["branch_name"] == branch_selected) &
            (df_sm["academic_year"] == "2026-27")
        ]
        
        if not sm_filtered.empty:
            display_sm = sm_filtered[[
                "institute_name", "branch_name", "total_intake",
                "state_seats", "minority_seats", "all_india_seats", "institute_seats"
            ]].rename(columns={
                "institute_name": "Institute",
                "branch_name": "Branch",
                "total_intake": "Total Intake",
                "state_seats": "MH State Seats",
                "minority_seats": "Minority",
                "all_india_seats": "All India (JEE)",
                "institute_seats": "Management / Inst."
            })
            st.dataframe(display_sm, use_container_width=True, hide_index=True)
        else:
            st.info("Seat matrix intake records not found for chosen combination.")
