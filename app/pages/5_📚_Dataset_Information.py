"""
Streamlit Page 5: Dataset Information & Source Traceability
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dataset Information", page_icon="📚", layout="wide")

st.title("📚 Dataset Information, Traceability & Limitations")
st.write("Complete audit trail of official Maharashtra State CET Cell documents, data dictionary, and validation metrics.")

tab1, tab2, tab3, tab4 = st.tabs(["📄 Source Manifest", "🔍 Data Quality Report", "📖 Category Guide", "⚖️ Ethics & Limitations"])

with tab1:
    st.subheader("Official PDF Documents & Manifest")
    st.write("All 18 official documents (14 CAP cutoff documents and 4 seat matrices) tracked across academic years:")
    try:
        df_manifest = pd.read_csv("docs/source_manifest.csv")
        st.dataframe(df_manifest[["academic_year", "document_type", "cap_round", "file_name", "status", "file_size_bytes"]], use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error loading manifest: {e}")

with tab2:
    st.subheader("Automated Data Quality & Integrity Checks")
    try:
        df_quality = pd.read_csv("dataset/processed/data_quality_report.csv")
        st.dataframe(df_quality, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error loading data quality report: {e}")

with tab3:
    st.subheader("Official Maharashtra Seat Category Definitions")
    category_info = [
        {"Code": "GOPENS", "Type": "General", "Category": "Open / General State Level", "Description": "Open merit seats available to all Maharashtra state candidates."},
        {"Code": "LOPENS", "Type": "Ladies", "Category": "Ladies Open State", "Description": "Seats reserved for female candidates in the Open category."},
        {"Code": "GOBCS", "Type": "General", "Category": "Other Backward Class", "Description": "General seats reserved for Maharashtra state OBC candidates."},
        {"Code": "LOBCS", "Type": "Ladies", "Category": "Ladies Other Backward Class", "Description": "Seats reserved for female OBC candidates."},
        {"Code": "EWS", "Type": "Special", "Category": "Economically Weaker Section", "Description": "10% over-and-above quota for candidates with family income < 8 LPA."},
        {"Code": "TFWS", "Type": "Tuition Fee Waiver", "Category": "Tuition Fee Waiver Scheme", "Description": "5% supernumerary quota with 100% tuition fee waiver for high merit students."},
        {"Code": "GSCS / LSCS", "Type": "General / Ladies", "Category": "Scheduled Caste", "Description": "Seats reserved for Maharashtra state SC candidates."},
        {"Code": "GSTS / LSTS", "Type": "General / Ladies", "Category": "Scheduled Tribe", "Description": "Seats reserved for Maharashtra state ST candidates."},
        {"Code": "GVJS / LVJS", "Type": "General / Ladies", "Category": "Vimukta Jati (VJ / DT-A)", "Description": "Seats reserved for DT-A category candidates."},
        {"Code": "GNT1S / 2S / 3S", "Type": "General", "Category": "Nomadic Tribes (NT-B, NT-C, NT-D)", "Description": "Seats reserved for specific Nomadic Tribe communities."}
    ]
    st.dataframe(pd.DataFrame(category_info), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Ethical Considerations, SDG Mapping & Limitations")
    st.markdown("""
    ### 🎯 Sustainable Development Goals (SDGs)
    - **SDG 4: Quality Education**: Fosters inclusive and equitable access to higher education information, eliminating information asymmetry for rural and first-generation college aspirants.
    - **SDG 10: Reduced Inequalities**: Provides transparent eligibility modeling and seat quota clarity across reserved categories (OBC, SC, ST, EWS, TFWS).

    ### ⚠️ System Limitations & Responsible AI Guidelines
    1. **Decision Support, Not Admission Guarantee**: The system estimates closing percentiles based on historical patterns. It cannot guarantee CAP allotment or simulate genuine probability without personal student application logs.
    2. **Autoregressive Constraints**: Cutoffs depend on dynamic annual applicant volumes, percentile distribution shifts, and seat intake changes introduced by DTE/AICTE.
    3. **Privacy by Design**: The application does NOT collect applicant names, roll numbers, application IDs, or uploaded certificates.
    """)
