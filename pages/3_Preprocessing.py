"""
Page 3: Data Quality & Preprocessing
====================================
Audits data coverage, handles calendar alignment, removes duplicates,
interpolates short gaps (<=2 weeks), preserves zeros, and standardizes series.
"""

import streamlit as st
import pandas as pd
from modules.state_manager import init_session_state, apply_custom_css, display_demo_warning
from modules.data_validation import validate_raw_dataset
from modules.preprocessing import preprocess_tourism_data

init_session_state()
apply_custom_css()

st.title("🧹 Data Quality & Preprocessing")
st.caption("Audit weekly data integrity, handle missing intervals, preserve zeros, and perform internal time-series standardization.")

display_demo_warning()

raw_df = st.session_state.get("raw_data")

if raw_df is None or raw_df.empty:
    st.warning("⚠️ No dataset has been uploaded yet. Please upload Google Trends CSV files on the Data Upload page or enable Demonstration Mode.")
    if st.button("Go to Data Upload"):
        st.switch_page("pages/2_Data_Upload.py")
    st.stop()

# Configuration Sidebar / Expander
with st.expander("⚙️ Preprocessing & Quality Threshold Parameters", expanded=True):
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        min_cov = st.slider(
            "Minimum Required Weekly Data Coverage (%)",
            min_value=50.0,
            max_value=100.0,
            value=float(st.session_state.get("min_coverage_pct", 80.0)),
            step=5.0,
            help="States/UTs with coverage below this threshold will be excluded from clustering."
        )
        st.session_state["min_coverage_pct"] = min_cov

    with col_p2:
        max_gap = st.number_input(
            "Maximum Consecutive Weeks to Interpolate (Short Gaps)",
            min_value=1,
            max_value=4,
            value=2,
            help="Strict limit: only short gaps of at most 2 weeks are linearly interpolated. Long gaps are preserved as missing."
        )

# Run Preprocessing Button
if st.button("Execute Data Preprocessing Pipeline", type="primary"):
    with st.spinner("Validating calendar alignment and applying internal standardization..."):
        audit, df_coverage = validate_raw_dataset(raw_df, min_coverage_pct=min_cov)
        cleaned_df, report = preprocess_tourism_data(raw_df, min_coverage_pct=min_cov, max_gap_weeks=max_gap)

        st.session_state["cleaned_data"] = cleaned_df
        st.session_state["preprocessing_report"] = report
        st.session_state["validation_audit"] = audit
        st.session_state["df_coverage"] = df_coverage

        st.success(f"Preprocessing completed! {len(report['eligible_regions'])} regions meet the {min_cov}% coverage requirement.")

# Display Results if available
cleaned_df = st.session_state.get("cleaned_data")
report = st.session_state.get("preprocessing_report")
df_cov = st.session_state.get("df_coverage")

if cleaned_df is not None and report is not None:
    st.markdown("---")
    st.subheader("Data Cleaning & Preprocessing Audit Summary")

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Original Records", f"{report['original_records']:,}")
    with m2:
        st.metric("Duplicates Removed", f"{report['duplicates_removed']:,}")
    with m3:
        st.metric("Short Gaps Filled", f"{report['short_gaps_interpolated']:,}", "≤2 wks")
    with m4:
        st.metric("Zeros Preserved", f"{report['zeros_preserved']:,}", "Low volume")
    with m5:
        st.metric("Eligible Regions", f"{len(report['eligible_regions'])}", f"-{len(report['excluded_regions'])} excluded")

    # Methodological Callout on Standardization
    st.markdown("""
        <div class="safeguard-banner">
            <strong>Methodological Note on Internal Standardization:</strong><br>
            Google Trends values are normalized relative-interest indices, not actual search counts. 
            Independently normalized regional exports cannot be compared directly as absolute search volume.
            To compare temporal and seasonal patterns fairly, the pipeline applies <strong>internal z-score standardization</strong> 
            (<em>mean = 0, std = 1</em>) to each (region, topic) series before seasonal feature construction.
        </div>
    """, unsafe_allow_html=True)

    # Coverage Table
    if df_cov is not None and not df_cov.empty:
        with st.expander("📊 View Regional Data Coverage Breakdown", expanded=False):
            st.dataframe(df_cov, use_container_width=True)

    # Cleaned Dataset Table
    st.subheader("Cleaned & Standardized Time Series Preview")
    st.dataframe(cleaned_df.head(20), use_container_width=True)

    # Download Button
    csv_bytes = cleaned_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Cleaned & Standardized Dataset (CSV)",
        data=csv_bytes,
        file_name="cleaned_tourism_trends.csv",
        mime="text/csv",
    )

