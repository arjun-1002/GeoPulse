"""
Page 6: PCA Dimensionality Reduction & Cluster Visualizations
==============================================================
Projects high-dimensional regional seasonal feature space into interactive
2D and 3D Principal Component Analysis (PCA) scatter plots using Plotly.
"""

import streamlit as st
import pandas as pd
from modules.state_manager import init_session_state, apply_custom_css, display_demo_warning
from modules.visualization import create_pca_scatter_2d, create_pca_scatter_3d

init_session_state()
apply_custom_css()

st.title("🗺️ PCA Dimensionality Reduction & Cluster Visualizations")
st.caption("Visualize high-dimensional regional tourism clusters in interactive 2D and 3D space via Principal Component Analysis.")

display_demo_warning()

df_scaled = st.session_state.get("df_scaled")
labels = st.session_state.get("labels")

if df_scaled is None or labels is None:
    st.warning("⚠️ Clustering has not been executed yet. Please run Clustering Analysis first.")
    if st.button("Go to Clustering Analysis"):
        st.switch_page("pages/5_Clustering.py")
    st.stop()

# Methodology Safeguard Note
st.markdown("""
    <div class="safeguard-banner">
        <strong>Important ML Principle:</strong> Clustering was performed on the <strong>complete multi-topic feature matrix</strong>, 
        NOT on the reduced PCA components. PCA is utilized strictly for post-hoc geometric visualization and variance inspection.
    </div>
""", unsafe_allow_html=True)

# 2D & 3D PCA Tabs
tab_2d, tab_3d = st.tabs(["📊 2D PCA Cluster Map", "🌐 3D PCA Interactive Projection"])

with tab_2d:
    fig_2d, pca_model, exp_var = create_pca_scatter_2d(
        df_scaled.values, labels, df_scaled.index.tolist(), n_components=2
    )
    st.plotly_chart(fig_2d, use_container_width=True)

    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.metric("PC1 Explained Variance", f"{exp_var[0]:.2f}%", "Dominant axis")
    with col_v2:
        st.metric("PC2 Explained Variance", f"{exp_var[1]:.2f}%", "Secondary axis")
    with col_v3:
        st.metric("Total 2D Retained Variance", f"{sum(exp_var):.2f}%", "Information preserved")

with tab_3d:
    if len(df_scaled) >= 3:
        fig_3d, exp_var_3d = create_pca_scatter_3d(
            df_scaled.values, labels, df_scaled.index.tolist()
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        st.info(f"The 3-component projection retains **{sum(exp_var_3d):.2f}%** of the total multidimensional variance across all features.")
    else:
        st.info("At least 3 observations are required for 3D PCA visualization.")

# PCA Theory & Interpretation Box
with st.expander("ℹ️ Understanding Principal Component Analysis (PCA)", expanded=False):
    st.markdown("""
        **What is Principal Component Analysis?**
        - Because our engineered dataset has many features (quarterly seasonal averages across multiple tourism domains), direct human visualization is impossible.
        - PCA finds the orthogonal axes of maximum variance in the standardized dataset.
        - **PC1 (Horizontal Axis):** Represents the primary direction of divergence between regional tourism search patterns.
        - **PC2 (Vertical Axis):** Captures the secondary orthogonal dimension of divergence.
        - High total explained variance indicates that the 2D scatter plot faithfully preserves the geometric relationships and cluster separation present in the original feature space.
    """)

