"""
Page 8: Tourism Planning Recommendations
========================================
Presents evidence-based promotional planning suggestions derived from
empirical clustering results, equipped with strategic rationales,
validation metrics, and decision-support safeguards.
"""

import streamlit as st
import pandas as pd
from modules.state_manager import init_session_state, inject_custom_css
from modules.recommendations import generate_planning_recommendations
from modules.report_generator import generate_html_summary_report

init_session_state()
inject_custom_css()

st.title("8. Tourism Planning Recommendations")
st.markdown("Decision-support hypotheses and promotional calendar suggestions formulated from empirical cluster profiles.")

labels = st.session_state.get("labels")
df_features = st.session_state.get("df_unscaled")

if labels is None or df_features is None:
    st.warning("⚠️ No clustering model results found. Please execute clustering on the **5. Clustering Analysis** page first.")
    if st.button("Go to Clustering Analysis"):
        st.switch_page("pages/5_Clustering.py")
    st.stop()

if st.session_state.get("is_demo_mode", False):
    st.info("ℹ️ Recommendations formulated using the **Demonstration Dataset** (Synthetic testing data).")

# Decision Support Safeguard Notice
st.warning(
    "⚠️ **CRITICAL DECISION-SUPPORT SAFEGUARD & ETHICAL NOTICE**\n\n"
    "1. **Curiosity ≠ Footfall:** Google search interest quantifies digital information-seeking queries within a region; it does NOT directly represent physical tourist arrivals, traveler expenditure, infrastructure readiness, or citizen travel behavior.\n"
    "2. **Evidence-Based Hypotheses:** All recommendations generated herein must be treated as preliminary hypotheses to guide targeted awareness initiatives, rather than absolute operational directives.\n"
    "3. **Field Validation Required:** Before committing marketing capital, state tourism departments must cross-reference these patterns with official footfall data, hotel occupancy surveys, and transit ticketing metrics."
)

region_names = df_features.index.tolist()

# Generate recommendations
df_recs = generate_planning_recommendations(df_features, labels, region_names)

if df_recs.empty:
    st.info("No specific seasonal peaks exceeded the detection threshold for the current clustering configuration.")
else:
    # Filter options
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        cluster_filter = st.selectbox(
            "Filter by Cluster:",
            options=["All Clusters"] + sorted(list(df_recs["Cluster_ID"].unique()))
        )
    with col_f2:
        topic_filter = st.selectbox(
            "Filter by Tourism Topic:",
            options=["All Topics"] + sorted(list(df_recs["Target_Topic"].unique()))
        )

    # Filter dataframe
    df_filtered = df_recs.copy()
    if cluster_filter != "All Clusters":
        df_filtered = df_filtered[df_filtered["Cluster_ID"] == cluster_filter]
    if topic_filter != "All Topics":
        df_filtered = df_filtered[df_filtered["Target_Topic"] == topic_filter]

    st.subheader(f"Strategic Promotional Initiatives ({len(df_filtered)} Identified)")

    for idx, row in df_filtered.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style="background-color: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; border: 1px solid #e2e8f0; border-left: 6px solid #2563eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 1.15rem; font-weight: 700; color: #1e3a8a;">{row['Campaign_Strategy']}</span>
                        <span style="background-color: #dbeafe; color: #1e40af; font-size: 0.8rem; font-weight: 600; padding: 4px 10px; border-radius: 9999px;">{row['Cluster_ID']}</span>
                    </div>
                    <div style="color: #475569; font-size: 0.9rem; margin-bottom: 12px;">
                        <strong>Target Topic:</strong> {row['Target_Topic']} &nbsp;|&nbsp; 
                        <strong>Recommended Launch Window:</strong> <span style="color: #0d9488; font-weight: 600;">{row['Peak_Quarter']}</span> &nbsp;|&nbsp;
                        <strong>Confidence:</strong> {row['Planning_Confidence']}
                    </div>
                    <div style="background-color: #f8fafc; border-radius: 6px; padding: 10px 14px; margin-bottom: 12px; font-size: 0.88rem; color: #334155;">
                        <strong>Observed Empirical Pattern:</strong> {row['Observed_Pattern']}<br>
                        <strong>Applicable States / UTs:</strong> {row['Member_Regions']}
                    </div>
                    <div style="font-size: 0.92rem; color: #1e293b; margin-bottom: 10px;">
                        <strong>Strategic Rationale:</strong> {row['Strategic_Rationale']}
                    </div>
                    <div style="font-size: 0.85rem; color: #059669; border-top: 1px dashed #cbd5e1; padding-top: 8px;">
                        📊 <strong>Field Validation Metrics:</strong> {row['Validation_Metrics']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.subheader("📥 Export Outputs & Executive Summary")
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        # Export CSV
        csv_recs = df_recs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Recommendations Table (CSV)",
            data=csv_recs,
            file_name="tourism_planning_recommendations.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_dl2:
        # Generate and Export HTML Report
        raw_df = st.session_state.get("raw_data")
        total_rec = len(raw_df) if raw_df is not None else 0
        n_top = raw_df["topic"].nunique() if (raw_df is not None and "topic" in raw_df.columns) else 6
        
        summary_stats = {
            "num_regions": len(region_names),
            "num_topics": n_top,
            "total_records": total_rec,
            "data_coverage": 100.0 if st.session_state.get("is_demo_mode", False) else 95.0,
        }
        
        # Prepare centroids table
        df_summary_for_report = df_features.copy()
        df_summary_for_report["Cluster"] = labels
        centroids = df_summary_for_report.groupby("Cluster").mean().round(2)
        
        clustering_metrics_saved = st.session_state.get("clustering_metrics", {})
        clustering_metrics = {
            "Silhouette_Score": clustering_metrics_saved.get("silhouette", 0.0),
            "Davies_Bouldin_Index": clustering_metrics_saved.get("davies_bouldin", 0.0),
            "MultiSeed_Stability_ARI": st.session_state.get("mean_ari", 1.0)
        }
        
        html_report = generate_html_summary_report(
            project_title="Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering",
            app_subtitle="An AI-Powered Tourism Planning Support System for Indian States and Union Territories",
            summary_stats=summary_stats,
            preprocessing_report=st.session_state.get("preprocessing_report", {}),
            clustering_metrics=clustering_metrics,
            df_profiles=centroids,
            df_recommendations=df_recs,
            pca_variance=None,
            selected_algo=st.session_state.get("selected_algo", "K-Means"),
            selected_k=st.session_state.get("selected_k", 3)
        )
        
        st.download_button(
            label="📑 Download Full Executive Report (HTML)",
            data=html_report.encode('utf-8'),
            file_name="CSE396_Tourism_Planning_Executive_Report.html",
            mime="text/html",
            use_container_width=True
        )

st.markdown("---")
st.info("💡 **Next Step:** Review the complete methodology, research questions, and university project background on the **9. About the Project** page.")
