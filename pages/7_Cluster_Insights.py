"""
Page 7: Cluster Insights
========================
Provides deep-dive profiling into regional cluster characteristics,
membership breakdowns, seasonal radar charts, and comparative profiles.
"""

import streamlit as st
import pandas as pd
import numpy as np
from modules.state_manager import init_session_state, inject_custom_css
from modules.visualization import create_cluster_size_bar, create_cluster_radar_profile, CLUSTER_COLORS
from modules.data_loader import TOPICS

init_session_state()
inject_custom_css()

st.title("7. Regional Cluster Insights & Profiles")
st.markdown("Detailed behavioral profiling of Indian States and Union Territories segmented by tourism search-interest patterns.")

labels = st.session_state.get("labels")
df_features = st.session_state.get("df_unscaled")

if labels is None or df_features is None:
    st.warning("⚠️ No clustering model results found. Please execute clustering on the **5. Clustering Analysis** page first.")
    if st.button("Go to Clustering Analysis"):
        st.switch_page("pages/5_Clustering.py")
    st.stop()

if st.session_state.get("is_demo_mode", False):
    st.info("ℹ️ Displaying insights for **Demonstration Dataset** (Synthetic Data for interface testing).")

region_names = df_features.index.tolist()
k = int(st.session_state.get("selected_k", len(set(labels))))

# Create summary dataframe with cluster labels
df_summary = df_features.copy()
df_summary["Region"] = region_names
df_summary["Cluster"] = labels
df_summary["Cluster_Name"] = [f"Cluster {l}" for l in labels]

# --- Overview Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Cluster Overview & Membership", "🧭 Seasonal Radar Profiles", "📋 Detailed Feature Means"])

with tab1:
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.subheader("Regional Membership Distribution")
        fig_bar = create_cluster_size_bar(labels)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_r:
        st.subheader("Cluster Membership Directory")
        for c in range(k):
            members = df_summary[df_summary["Cluster"] == c]["Region"].tolist()
            with st.expander(f"📍 Cluster {c} ({len(members)} States / UTs)", expanded=(c == 0)):
                st.write(", ".join(sorted(members)))
                # Show top dominant topic for this cluster
                c_means = df_features[labels == c].mean()
                mean_cols = [c for c in c_means.index if c.endswith("_Mean")]
                if mean_cols:
                    top_topic_col = c_means[mean_cols].idxmax()
                    top_topic_name = top_topic_col.replace("_Mean", "")
                    st.caption(f"**Dominant Interest Topic:** {top_topic_name} (Z-score Mean: {c_means[top_topic_col]:+.2f})")

    st.markdown("---")
    st.subheader("Individual Region Lookup")
    selected_reg = st.selectbox("Select State / Union Territory to view assignment and statistics:", options=sorted(region_names))
    reg_row = df_summary[df_summary["Region"] == selected_reg].iloc[0]
    reg_cluster = reg_row["Cluster"]
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Assigned Cluster", f"Cluster {reg_cluster}")
    with c2:
        st.metric("Peers in Cluster", f"{sum(labels == reg_cluster) - 1} other states")
    with c3:
        # Find highest Q for this state
        q_cols = [col for col in df_features.columns if any(col.endswith(f"_{q}") for q in ["Q1", "Q2", "Q3", "Q4"])]
        if q_cols:
            max_q_col = reg_row[q_cols].idxmax()
            st.metric("Highest Seasonal Search", max_q_col)
        else:
            st.metric("Highest Seasonal Search", "N/A")
    with c4:
        st.metric("Algorithm Used", st.session_state.get("selected_algo", "K-Means"))

with tab2:
    st.subheader("Seasonal Interest Radar Fingerprint")
    st.markdown(
        "Standardized seasonal comparison (Q1: Jan–Mar, Q2: Apr–Jun, Q3: Jul–Sep, Q4: Oct–Dec) "
        "across tourism topics. Values above 0 represent above-average seasonal search interest."
    )
    fig_radar = create_cluster_radar_profile(df_features, labels, TOPICS)
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.caption(
        "📌 **Interpretation Note:** Radar radii reflect within-region standardized Z-scores. "
        "A higher radial spike demonstrates that during that specific calendar quarter, Google search volume "
        "for that topic is significantly higher than that region's annual baseline."
    )

with tab3:
    st.subheader("Cluster Feature Profiles (Centroid Means)")
    st.markdown("Mean engineered feature values for each cluster across all 42 indicators.")
    
    cluster_means_table = df_features.copy()
    cluster_means_table["Cluster"] = [f"Cluster {l}" for l in labels]
    grouped_means = cluster_means_table.groupby("Cluster").mean().round(3)
    
    st.dataframe(grouped_means, use_container_width=True)
    
    # Download centroids CSV
    csv_centroids = grouped_means.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Download Cluster Centroids Table (CSV)",
        data=csv_centroids,
        file_name="cluster_centroid_profiles.csv",
        mime="text/csv",
    )

st.markdown("---")
st.info(
    "💡 **Next Step:** Explore evidence-based promotional campaign hypotheses derived from these cluster profiles on the "
    "**8. Tourism Planning Recommendations** page."
)
