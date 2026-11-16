"""
Streamlit Page 1: Personalized Recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.recommendations.recommendation_engine import MHTCETRecommender
from app.utils.display_helpers import get_badge_html, format_gap
from app.utils.input_validation import validate_percentile

st.set_page_config(page_title="Personalized Recommendations", page_icon="🎯", layout="wide")

st.title("🎯 Personalized Engineering College Recommendations")
st.write("Enter your MHT-CET PCM percentile and preferences to receive transparent, AI-forecasted college shortlists.")

@st.cache_resource
def get_recommender():
    return MHTCETRecommender()

recommender = get_recommender()

# Sidebar Student Profile Input Form
with st.sidebar:
    st.header("👤 Candidate Admission Profile")
    
    percentile_input = st.number_input(
        "MHT-CET PCM Percentile (0.00 - 100.00)",
        min_value=0.0,
        max_value=100.0,
        value=92.50,
        step=0.05,
        format="%.2f"
    )
    
    categories = recommender.get_supported_categories()
    category_input = st.selectbox(
        "Eligible Seat Category Code",
        options=categories,
        index=categories.index("GOPENS") if "GOPENS" in categories else 0
    )
    
    pools = recommender.get_supported_pools()
    pool_input = st.selectbox(
        "Eligible Seat Pool",
        options=pools,
        index=pools.index("State Level") if "State Level" in pools else 0
    )
    
    cap_round = st.radio(
        "Target CAP Round",
        options=[1, 2, 3, 4],
        index=0,
        horizontal=True
    )
    
    branches = recommender.get_supported_branches()
    selected_branches = st.multiselect(
        "Preferred Engineering Branches",
        options=branches,
        default=[b for b in branches if "Computer" in b or "Information" in b or "Artificial" in b]
    )
    
    regions = recommender.get_supported_regions()
    selected_regions = st.multiselect(
        "Preferred Regions/Cities (Optional)",
        options=regions,
        default=[]
    )
    
    top_n = st.slider("Maximum Shortlisted Options", min_value=5, max_value=50, value=20, step=5)
    
    btn_predict = st.button("🚀 Generate Personalized Shortlist", type="primary", use_container_width=True)

# Run Recommendation
is_valid, pct_val = validate_percentile(percentile_input)
if not is_valid:
    st.error(pct_val)
else:
    with st.spinner("Analyzing cutoff patterns & computing AI estimates..."):
        res = recommender.recommend(
            student_percentile=pct_val,
            seat_category=category_input,
            seat_pool=pool_input,
            preferred_branches=selected_branches if selected_branches else None,
            preferred_regions=selected_regions if selected_regions else None,
            cap_round=cap_round,
            top_n=top_n
        )
        
    if res["status"] == "error":
        st.error(res["message"])
    elif res["status"] == "no_results":
        st.warning(res["message"])
    else:
        recs = res["recommendations"]
        df_rec = pd.DataFrame(recs)
        
        # Summary KPI cards
        col_s, col_m, col_r, col_tot = st.columns(4)
        n_safer = (df_rec["suitability_group"] == "Safer").sum() if not df_rec.empty else 0
        n_mod = (df_rec["suitability_group"] == "Moderate").sum() if not df_rec.empty else 0
        n_reach = (df_rec["suitability_group"] == "Reach").sum() if not df_rec.empty else 0
        
        col_s.metric("🛡️ Safer Options", n_safer, help="Student percentile is comfortably above predicted cutoff")
        col_m.metric("⚖️ Moderate Options", n_mod, help="Competitive options within model error margin")
        col_r.metric("🚀 Reach Options", n_reach, help="Ambitious choices where cutoff is slightly above score")
        col_tot.metric("📋 Total Evaluated", len(df_rec))
        
        st.write("")
        
        # Tabular View with Explanations
        st.subheader("📋 Option List & Suitability Breakdown")
        
        # Filter tabs
        view_filter = st.radio(
            "Filter Display by Group:",
            options=["All Options", "Safer Only", "Moderate Only", "Reach Only"],
            horizontal=True
        )
        
        df_display = df_rec.copy()
        if view_filter == "Safer Only":
            df_display = df_display[df_display["suitability_group"] == "Safer"]
        elif view_filter == "Moderate Only":
            df_display = df_display[df_display["suitability_group"] == "Moderate"]
        elif view_filter == "Reach Only":
            df_display = df_display[df_display["suitability_group"] == "Reach"]
            
        display_cols = [
            "suitability_group", "institute_name", "branch_name", "region",
            "predicted_cutoff", "student_percentile", "percentile_gap", "history_2026", "explanation"
        ]
        
        # Render clean interactive dataframe
        st.dataframe(
            df_display[display_cols].rename(columns={
                "suitability_group": "Suitability",
                "institute_name": "Institute",
                "branch_name": "Branch",
                "region": "City/Region",
                "predicted_cutoff": "Predicted Cutoff (2027)",
                "student_percentile": "Your Score",
                "percentile_gap": "Gap (%)",
                "history_2026": "2026 Cutoff",
                "explanation": "Recommendation Rationale"
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # CSV Download Button
        csv_data = df_display[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CAP Option Shortlist (CSV)",
            data=csv_data,
            file_name=f"mht_cet_shortlist_p{pct_val}_{category_input}.csv",
            mime="text/csv"
        )
        
        st.divider()
        st.subheader("💡 How Are These Suitability Labels Calculated?")
        st.markdown(f"""
        - **Safer Options**: Your percentile is above the predicted cutoff by more than the model error margin ($\Delta > {res['margin']:.2f}\%$).
        - **Moderate Options**: Your percentile is within the competitive error band ($|\Delta| \le {res['margin']:.2f}\%$).
        - **Reach Options**: The predicted cutoff is higher than your current score ($\Delta < -{res['margin']:.2f}\%$).
        """)
