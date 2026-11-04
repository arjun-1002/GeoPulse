"""
Page 2: Data Upload & Consolidation
====================================
Upload multiple Google Trends CSV files, automatically infer or manually
assign regions and topics, preview consolidated dataset, and export metadata logs.
"""

import streamlit as st
import pandas as pd
from modules.state_manager import init_session_state, apply_custom_css, display_demo_warning
from modules.data_loader import (
    VALID_TOPICS, INDIAN_REGIONS, infer_metadata_from_filename,
    consolidate_uploaded_files, generate_synthetic_demo_dataset
)
from modules.data_validation import validate_raw_dataset

init_session_state()
apply_custom_css()

st.title("📥 Data Upload & Consolidation")
st.caption("Upload multiple exported Google Trends CSV files for Indian States/UTs across the 6 selected tourism topics.")

display_demo_warning()

# Instructions & Format Guide
with st.expander("ℹ️ Google Trends Export Format & Topic Guide", expanded=False):
    st.markdown("""
        **Required Data Specifications:**
        - **Geographic Scope:** Indian States & Union Territories.
        - **Frequency:** Weekly search interest data.
        - **Timeframe:** November 2023 to November 2026.
        - **Standard Topics:** `Tourism`, `Travel`, `Beaches`, `Hill stations`, `Wildlife tourism`, `Religious tourism`.
        - **File Format:** Native Google Trends `.csv` exports (the system automatically skips introductory metadata headers).
    """)

# Demonstration Mode Shortcut
col_demo1, col_demo2 = st.columns([3, 1])
with col_demo1:
    st.write("Don't have Google Trends CSV files ready? You can load the verified Demonstration Dataset:")
with col_demo2:
    if st.button("🧪 Load Demo Dataset", use_container_width=True):
        demo_df = generate_synthetic_demo_dataset()
        st.session_state["raw_data"] = demo_df
        st.session_state["is_demo_mode"] = True
        st.success("Demonstration dataset loaded! Proceed to Preprocessing.")
        st.rerun()

st.markdown("---")

# File Uploader
uploaded_files = st.file_uploader(
    "Choose Google Trends CSV Files",
    type=["csv"],
    accept_multiple_files=True,
    help="Select one or more exported CSV files from Google Trends."
)

if uploaded_files:
    st.subheader(f"Uploaded Files ({len(uploaded_files)} files)")
    st.write("Verify or adjust the inferred Region and Topic for each file before consolidating:")

    # Map filename to inferred values
    user_assignments = {}
    
    with st.form("file_assignment_form"):
        for uf in uploaded_files:
            inf_region, inf_topic = infer_metadata_from_filename(uf.name)
            
            c_fn, c_reg, c_top = st.columns([2, 1.5, 1.5])
            with c_fn:
                st.text(uf.name)
            with c_reg:
                default_reg_idx = INDIAN_REGIONS.index(inf_region) if inf_region in INDIAN_REGIONS else 0
                sel_region = st.selectbox(
                    f"Region for {uf.name}",
                    INDIAN_REGIONS,
                    index=default_reg_idx,
                    key=f"reg_{uf.name}",
                    label_visibility="collapsed"
                )
            with c_top:
                default_top_idx = VALID_TOPICS.index(inf_topic) if inf_topic in VALID_TOPICS else 0
                sel_topic = st.selectbox(
                    f"Topic for {uf.name}",
                    VALID_TOPICS,
                    index=default_top_idx,
                    key=f"top_{uf.name}",
                    label_visibility="collapsed"
                )

            user_assignments[uf.name] = {"region": sel_region, "topic": sel_topic}

        submitted = st.form_submit_button("Consolidate Uploaded Files", type="primary")

    if submitted:
        with st.spinner("Parsing and consolidating files..."):
            consolidated_df, meta_df = consolidate_uploaded_files(uploaded_files, user_assignments)
            
            if consolidated_df.empty:
                st.error("Could not parse any valid search interest series from the uploaded files.")
            else:
                st.session_state["raw_data"] = consolidated_df
                st.session_state["metadata_log"] = meta_df
                st.session_state["is_demo_mode"] = False
                st.success(f"Successfully consolidated {len(consolidated_df):,} weekly observations across {consolidated_df['region'].nunique()} regions!")
                st.rerun()

# Display Current Raw Dataset
current_raw = st.session_state.get("raw_data")
if current_raw is not None and not current_raw.empty:
    st.markdown("---")
    st.subheader("Current Consolidated Raw Dataset Preview")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total Records", f"{len(current_raw):,}")
    with col_stat2:
        st.metric("Covered Regions", f"{current_raw['region'].nunique()} States/UTs")
    with col_stat3:
        st.metric("Covered Topics", f"{current_raw['topic'].nunique()} Topics")

    st.dataframe(current_raw.head(25), use_container_width=True)

    # Download consolidated data
    csv_bytes = current_raw.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Consolidated Raw Dataset (CSV)",
        data=csv_bytes,
        file_name="consolidated_google_trends_raw.csv",
        mime="text/csv",
    )

    # Metadata Log
    meta_log = st.session_state.get("metadata_log")
    if meta_log is not None and not meta_log.empty:
        with st.expander("📄 View Upload Metadata Log"):
            st.dataframe(meta_log, use_container_width=True)
            meta_bytes = meta_log.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Upload Metadata Log (CSV)",
                data=meta_bytes,
                file_name="upload_metadata_log.csv",
                mime="text/csv",
            )

