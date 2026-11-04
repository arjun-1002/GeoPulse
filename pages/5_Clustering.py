"""
Page 5: Clustering Analysis & Multi-Metric Validation
=====================================================
Applies K-Means (Euclidean L2) and K-Medians (Manhattan L1), evaluates
WCSS / L1 cost, Silhouette Score, Davies-Bouldin Index, and computes ARI stability.
"""

import streamlit as st
import pandas as pd
import numpy as np
from modules.state_manager import init_session_state, apply_custom_css, display_demo_warning
from modules.clustering import (
    run_clustering, evaluate_kmeans_models, evaluate_kmedians_models, assess_cluster_stability
)
from modules.visualization import (
    create_elbow_plot, create_metrics_comparison_plot, create_cluster_size_bar
)
from modules.recommendations import generate_planning_recommendations

init_session_state()
apply_custom_css()

st.title("🔬 Clustering Analysis & Validation")
st.caption("Apply unsupervised K-Means (Euclidean L2) and K-Medians (Manhattan L1) across candidate cluster counts with rigorous multi-metric validation.")

display_demo_warning()

df_scaled = st.session_state.get("df_scaled")
df_unscaled = st.session_state.get("df_unscaled")

if df_scaled is None or df_scaled.empty:
    st.warning("⚠️ Regional feature matrix is not available. Please complete Feature Engineering first.")
    if st.button("Go to Feature Engineering"):
        st.switch_page("pages/4_Feature_Engineering.py")
    st.stop()

n_regions = len(df_scaled)
if n_regions < 2:
    st.error(f"Clustering requires at least 2 eligible regions. Currently only {n_regions} region is available.")
    st.stop()

# Algorithm and K Selection Bar
col_algo, col_k = st.columns(2)
with col_algo:
    algo_choice = st.selectbox(
        "Select Clustering Algorithm",
        ["K-Means", "K-Medians"],
        index=0 if st.session_state.get("selected_algo") == "K-Means" else 1,
        help="K-Means uses Euclidean distance (L2); K-Medians uses Manhattan distance (L1) and coordinate-wise medians."
    )
    st.session_state["selected_algo"] = algo_choice

with col_k:
    max_k = min(5, n_regions - 1)
    k_choice = st.slider(
        "Select Number of Clusters (K)",
        min_value=2,
        max_value=max_k,
        value=int(min(st.session_state.get("selected_k", 3), max_k)),
        help="Candidate K values typically range from 2 to 5."
    )
    st.session_state["selected_k"] = k_choice

# Academic Geometry Distinction Callout
if algo_choice == "K-Means":
    st.markdown("""
        <div class="safeguard-banner">
            <strong>K-Means (Euclidean Geometry L2):</strong> Centroids are computed as the <em>arithmetic mean</em> of cluster members. 
            The arithmetic mean uniquely minimizes Within-Cluster Sum of Squares (WCSS / Inertia).
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="safeguard-banner">
            <strong>K-Medians (Manhattan Geometry L1):</strong> Centroids are computed as the <em>coordinate-wise median</em> of cluster members. 
            The median uniquely minimizes total absolute Manhattan distance (L1 norm). It is more robust to regional outliers.
        </div>
    """, unsafe_allow_html=True)

# Run Clustering Button
if st.button("Execute Clustering & Multi-Metric Evaluation", type="primary"):
    with st.spinner(f"Fitting {algo_choice} (K={k_choice}) and computing validation metrics..."):
        X = df_scaled.values
        labels, model, metrics = run_clustering(X, algorithm=algo_choice, k=k_choice)
        st.session_state["labels"] = labels
        st.session_state["clustering_metrics"] = metrics

        # Multi-K evaluation
        df_km, _ = evaluate_kmeans_models(X)
        df_kmed, _ = evaluate_kmedians_models(X)
        st.session_state["df_eval_kmeans"] = df_km
        st.session_state["df_eval_kmedians"] = df_kmed

        # Stability
        mean_ari, df_stab = assess_cluster_stability(X, algorithm=algo_choice, k=k_choice)
        st.session_state["mean_ari"] = mean_ari
        st.session_state["df_stability"] = df_stab

        # Update Recommendations
        if df_unscaled is not None:
            recs = generate_planning_recommendations(df_unscaled, labels, df_scaled.index.tolist())
            st.session_state["recommendations"] = recs

        st.success(f"Clustering completed successfully! Silhouette Score: {metrics['silhouette']:.4f}")

# Display Active Clustering Results
labels = st.session_state.get("labels")
metrics = st.session_state.get("clustering_metrics")

if labels is not None and metrics is not None:
    st.markdown("---")
    st.subheader(f"Active Model Validation: {metrics['algorithm']} (K = {metrics['k']})")

    # Metrics Summary Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        cost_label = "WCSS (Inertia)" if metrics["algorithm"] == "K-Means" else "Total L1 Cost"
        st.metric(cost_label, f"{metrics['cost']:,.1f}", "Compactness")
    with m2:
        st.metric("Silhouette Score", f"{metrics['silhouette']:.4f}", "Higher is better")
    with m3:
        st.metric("Davies-Bouldin Index", f"{metrics['davies_bouldin']:.4f}", "Lower is better")
    with m4:
        mean_ari = st.session_state.get("mean_ari", 1.0)
        st.metric("Stability (Mean ARI)", f"{mean_ari:.4f}", "10 Random Seeds")

    # Visualizations: Cluster Sizes and Multi-K Comparison
    c_left, c_right = st.columns([1, 1.4])
    with c_left:
        fig_sizes = create_cluster_size_bar(labels)
        st.plotly_chart(fig_sizes, use_container_width=True)

    with c_right:
        active_eval_df = st.session_state["df_eval_kmeans"] if metrics["algorithm"] == "K-Means" else st.session_state["df_eval_kmedians"]
        if active_eval_df is not None:
            fig_elbow = create_elbow_plot(active_eval_df)
            st.plotly_chart(fig_elbow, use_container_width=True)

    # Multi-K Comparison Table
    st.subheader("Multi-K Validation Comparison Table")
    if active_eval_df is not None:
        st.dataframe(active_eval_df, use_container_width=True)
        csv_eval = active_eval_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Validation Comparison Metrics (CSV)",
            data=csv_eval,
            file_name="clustering_evaluation_metrics.csv",
            mime="text/csv",
        )

    # Cluster Assignment Table
    st.subheader("Regional Cluster Assignments")
    df_assignments = pd.DataFrame({
        "Region (State/UT)": df_scaled.index,
        "Cluster Assignment": [f"Cluster {l}" for l in labels],
        "Cluster_ID": labels
    }).sort_values(["Cluster_ID", "Region (State/UT)"])

    st.dataframe(df_assignments, use_container_width=True)

    csv_assign = df_assignments.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Cluster Assignments (CSV)",
        data=csv_assign,
        file_name="regional_cluster_assignments.csv",
        mime="text/csv",
    )

