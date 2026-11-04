"""
Page 1: Home Dashboard
=======================
Executive summary view displaying core metrics, project identity,
safeguard banners, and direct navigation links to analysis pages.
"""

import streamlit as st
import pandas as pd
from modules.state_manager import init_session_state, apply_custom_css, display_demo_warning
from modules.data_loader import generate_synthetic_demo_dataset
from modules.preprocessing import preprocess_tourism_data
from modules.feature_engineering import construct_regional_features
from modules.clustering import run_clustering, evaluate_kmeans_models, evaluate_kmedians_models, assess_cluster_stability
from modules.recommendations import generate_planning_recommendations

init_session_state()
apply_custom_css()

# Hero Header
st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering</div>
        <div class="hero-subtitle">Regional Tourism Promotion Planner — An AI-Powered Planning Support System for Indian States and Union Territories</div>
        <div class="hero-desc">
            An unsupervised machine learning system designed to discover natural groupings of Indian States and Union Territories
            based on seasonal and temporal Google Search interest patterns across six critical tourism domains.
        </div>
    </div>
""", unsafe_allow_html=True)

display_demo_warning()

# Ethical Safeguard Banner
st.markdown("""
    <div class="safeguard-banner">
        <strong>Decision-Support Safeguard:</strong> This application is intended as a strategic planning aid for state and national tourism departments. 
        Google Trends data reflects relative online curiosity, not actual tourist footfall, bookings, or revenue. 
        All suggestions must be evaluated through empirical field validation.
    </div>
""", unsafe_allow_html=True)

raw_df = st.session_state.get("raw_data")

if raw_df is None or raw_df.empty:
    # Empty State - Welcome & Demo Launcher
    st.info("👋 **Welcome! No Google Trends dataset has been uploaded yet.** You can upload your weekly Google Trends CSV files or test the complete interface using the Demonstration Mode.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📥 Option A: Upload Real Data")
        st.write("Upload exported Google Trends CSV files covering Indian States and Union Territories across tourism topics.")
        if st.button("Go to Data Upload Page", type="primary", use_container_width=True):
            st.switch_page("pages/2_Data_Upload.py")

    with col2:
        st.markdown("### 🧪 Option B: Demonstration Mode")
        st.write("Instantly generate a realistic synthetic demonstration dataset (24 states, 6 topics, 2023–2026 weekly series) to explore the entire UI and ML pipeline.")
        if st.button("Load Demonstration Dataset (Synthetic)", use_container_width=True):
            with st.spinner("Generating demonstration dataset & running full pipeline..."):
                demo_raw = generate_synthetic_demo_dataset()
                st.session_state["raw_data"] = demo_raw
                st.session_state["is_demo_mode"] = True

                # Preprocess & engineer features automatically for demo
                df_clean, report = preprocess_tourism_data(demo_raw, min_coverage_pct=80.0)
                st.session_state["cleaned_data"] = df_clean
                st.session_state["preprocessing_report"] = report

                df_unscaled, df_scaled, scaler, f_info = construct_regional_features(df_clean)
                st.session_state["df_unscaled"] = df_unscaled
                st.session_state["df_scaled"] = df_scaled
                st.session_state["scaler"] = scaler
                st.session_state["feature_info"] = f_info

                # Run baseline clustering
                labels, model, metrics = run_clustering(df_scaled.values, algorithm="K-Means", k=3)
                st.session_state["labels"] = labels
                st.session_state["clustering_metrics"] = metrics
                st.session_state["selected_algo"] = "K-Means"
                st.session_state["selected_k"] = 3

                # Evaluate models across K
                df_km, _ = evaluate_kmeans_models(df_scaled.values)
                df_kmed, _ = evaluate_kmedians_models(df_scaled.values)
                st.session_state["df_eval_kmeans"] = df_km
                st.session_state["df_eval_kmedians"] = df_kmed

                # Stability
                mean_ari, df_stab = assess_cluster_stability(df_scaled.values, algorithm="K-Means", k=3)
                st.session_state["mean_ari"] = mean_ari
                st.session_state["df_stability"] = df_stab

                # Recommendations
                recs = generate_planning_recommendations(df_unscaled, labels, df_scaled.index.tolist())
                st.session_state["recommendations"] = recs

                st.success("Demonstration dataset loaded and processed successfully!")
                st.rerun()

else:
    # Dataset is loaded - Display Active Dashboard Statistics
    cleaned_df = st.session_state.get("cleaned_data")
    df_scaled = st.session_state.get("df_scaled")
    metrics = st.session_state.get("clustering_metrics", {})
    selected_k = st.session_state.get("selected_k", 3)
    selected_algo = st.session_state.get("selected_algo", "K-Means")

    n_regions = raw_df["region"].nunique()
    n_topics = raw_df["topic"].nunique()
    n_records = len(raw_df)
    n_eligible = len(df_scaled) if df_scaled is not None else (len(st.session_state["preprocessing_report"]["eligible_regions"]) if st.session_state.get("preprocessing_report") else n_regions)

    # 4 Key Metrics Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Regions", f"{n_regions} States/UTs", f"{n_eligible} Eligible")
    with m2:
        st.metric("Tourism Topics", f"{n_topics} Topics", "6 Standardized")
    with m3:
        st.metric("Total Observations", f"{n_records:,} Records", "Weekly Freq")
    with m4:
        sil_score = metrics.get("silhouette", "N/A")
        sil_str = f"{sil_score:.4f}" if isinstance(sil_score, (int, float)) else str(sil_score)
        st.metric("Active Model", f"{selected_algo} (K={selected_k})", f"Sil: {sil_str}")

    st.markdown("---")

    # Quick Navigation Grid
    st.subheader("Explore Application Modules")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("#### 📥 Data Upload")
        st.caption("Upload and consolidate raw Google Trends CSV files.")
        if st.button("Go to Upload", use_container_width=True):
            st.switch_page("pages/2_Data_Upload.py")
    with c2:
        st.markdown("#### 🧹 Preprocessing")
        st.caption("Inspect data quality, missing weeks, and gap interpolation.")
        if st.button("Go to Preprocessing", use_container_width=True):
            st.switch_page("pages/3_Preprocessing.py")
    with c3:
        st.markdown("#### ⚙️ Feature Matrix")
        st.caption("Review quarterly seasonality, volatility, and trend features.")
        if st.button("Go to Features", use_container_width=True):
            st.switch_page("pages/4_Feature_Engineering.py")
    with c4:
        st.markdown("#### 🔬 Clustering Analysis")
        st.caption("Run K-Means & K-Medians with multi-metric validation.")
        if st.button("Go to Clustering", use_container_width=True):
            st.switch_page("pages/5_Clustering.py")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.markdown("#### 🗺️ PCA Projection")
        st.caption("Explore interactive 2D and 3D cluster visualizations.")
        if st.button("Go to PCA Map", use_container_width=True):
            st.switch_page("pages/6_PCA_Visualization.py")
    with c6:
        st.markdown("#### 💡 Cluster Insights")
        st.caption("Inspect cluster membership and seasonal radar profiles.")
        if st.button("Go to Insights", use_container_width=True):
            st.switch_page("pages/7_Cluster_Insights.py")
    with c7:
        st.markdown("#### 🎯 Planning Support")
        st.caption("Actionable tourism promotion campaign suggestions.")
        if st.button("Go to Recommendations", use_container_width=True):
            st.switch_page("pages/8_Planning_Recommendations.py")
    with c8:
        st.markdown("#### ℹ️ Project Context")
        st.caption("Academic problem statement, methodology & limitations.")
        if st.button("Go to About", use_container_width=True):
            st.switch_page("pages/9_About.py")

