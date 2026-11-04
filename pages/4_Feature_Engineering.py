"""
Page 4: Feature Engineering
============================
Transforms longitudinal weekly time series into a regional feature matrix
(one row per State/UT) measuring quarterly seasonal intensity, volatility, and trend slopes.
"""

import streamlit as st
import pandas as pd
from modules.state_manager import init_session_state, apply_custom_css, display_demo_warning
from modules.feature_engineering import construct_regional_features

init_session_state()
apply_custom_css()

st.title("⚙️ Regional Feature Engineering")
st.caption("Construct a regional feature matrix (one observation per State/UT) capturing quarterly seasonal demand, volatility, and annual trends.")

display_demo_warning()

cleaned_df = st.session_state.get("cleaned_data")

if cleaned_df is None or cleaned_df.empty:
    st.warning("⚠️ Cleaned data is not available yet. Please complete the Preprocessing step first.")
    if st.button("Go to Preprocessing"):
        st.switch_page("pages/3_Preprocessing.py")
    st.stop()

# Feature Construction Button
if st.button("Construct Regional Feature Matrix", type="primary"):
    with st.spinner("Extracting quarterly seasonality, volatility, and trend features per region..."):
        df_unscaled, df_scaled, scaler, feature_info = construct_regional_features(cleaned_df)
        st.session_state["df_unscaled"] = df_unscaled
        st.session_state["df_scaled"] = df_scaled
        st.session_state["scaler"] = scaler
        st.session_state["feature_info"] = feature_info
        st.success(f"Feature matrix generated! Extracted {df_scaled.shape[1]} features across {df_scaled.shape[0]} eligible Indian States/UTs.")

df_scaled = st.session_state.get("df_scaled")
df_unscaled = st.session_state.get("df_unscaled")
f_info = st.session_state.get("feature_info", {})

if df_scaled is not None and not df_scaled.empty:
    st.markdown("---")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.metric("Total Regional Observations (Rows)", f"{df_scaled.shape[0]} States/UTs")
    with col_f2:
        st.metric("Engineered Features (Columns)", f"{df_scaled.shape[1]} Features")

    st.markdown("""
        <div class="safeguard-banner">
            <strong>Key Architecture Rule:</strong> Clustering is performed at the <strong>regional level</strong> (one row per state/UT), 
            NOT by clustering individual weeks or individual topics. This clusters Indian states by their multi-topic seasonal fingerprint.
        </div>
    """, unsafe_allow_html=True)

    tab_scaled, tab_unscaled, tab_dict = st.tabs(["Standardized Feature Matrix (For Clustering)", "Unscaled Feature Matrix", "Feature Dictionary"])

    with tab_scaled:
        st.caption("Scaled using StandardScaler (mean = 0, variance = 1) ensuring equal weighting across seasonal and trend features:")
        st.dataframe(df_scaled.round(3), use_container_width=True)
        csv_scaled = df_scaled.to_csv().encode("utf-8")
        st.download_button(
            label="⬇️ Download Scaled Feature Matrix (CSV)",
            data=csv_scaled,
            file_name="regional_features_scaled.csv",
            mime="text/csv",
        )

    with tab_unscaled:
        st.caption("Raw engineered features (quarterly standardized interest averages, volatility std, OLS slopes):")
        st.dataframe(df_unscaled.round(3), use_container_width=True)
        csv_unscaled = df_unscaled.to_csv().encode("utf-8")
        st.download_button(
            label="⬇️ Download Unscaled Feature Matrix (CSV)",
            data=csv_unscaled,
            file_name="regional_features_unscaled.csv",
            mime="text/csv",
        )

    with tab_dict:
        st.caption("Definitions of all engineered seasonal, volatility, and trend features:")
        dict_rows = [{"Feature Name": k, "Description": v} for k, v in f_info.items()]
        st.dataframe(pd.DataFrame(dict_rows), use_container_width=True)

