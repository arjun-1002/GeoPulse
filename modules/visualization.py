"""
Visualization Module for Tourism Planning Dashboard
===================================================
Produces interactive Plotly charts for PCA projections, Elbow curves,
evaluation metrics, seasonal radar profiles, and time series trends.
"""

import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np


# Palette for clusters
CLUSTER_COLORS = ["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"]


def create_pca_scatter_2d(X_scaled, labels, region_names, n_components=2):
    """
    Generate an interactive 2D PCA scatter plot using Plotly.
    """
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    exp_var = pca.explained_variance_ratio_ * 100

    df_plot = pd.DataFrame({
        "PC1": X_pca[:, 0],
        "PC2": X_pca[:, 1],
        "Region": region_names,
        "Cluster": [f"Cluster {l}" for l in labels],
        "Cluster_ID": labels
    })

    fig = px.scatter(
        df_plot,
        x="PC1",
        y="PC2",
        color="Cluster",
        text="Region",
        hover_name="Region",
        hover_data={"PC1": ":.2f", "PC2": ":.2f", "Cluster": True},
        color_discrete_sequence=CLUSTER_COLORS,
        title=f"2D PCA Projection of Tourism Search-Interest Clusters<br><sup>Total Retained Variance: {sum(exp_var):.2f}% (PC1: {exp_var[0]:.2f}%, PC2: {exp_var[1]:.2f}%)</sup>",
    )

    fig.update_traces(
        textposition="top right",
        textfont=dict(size=10),
        marker=dict(size=12, line=dict(width=1, color="DarkSlateGrey"), opacity=0.85)
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title=f"Principal Component 1 ({exp_var[0]:.2f}% Variance)",
        yaxis_title=f"Principal Component 2 ({exp_var[1]:.2f}% Variance)",
        legend_title="Cluster Segment",
        height=580,
    )

    return fig, pca, exp_var


def create_pca_scatter_3d(X_scaled, labels, region_names):
    """
    Generate an interactive 3D PCA scatter plot using Plotly.
    """
    pca = PCA(n_components=3, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    exp_var = pca.explained_variance_ratio_ * 100

    df_plot = pd.DataFrame({
        "PC1": X_pca[:, 0],
        "PC2": X_pca[:, 1],
        "PC3": X_pca[:, 2],
        "Region": region_names,
        "Cluster": [f"Cluster {l}" for l in labels],
    })

    fig = px.scatter_3d(
        df_plot,
        x="PC1",
        y="PC2",
        z="PC3",
        color="Cluster",
        text="Region",
        hover_name="Region",
        color_discrete_sequence=CLUSTER_COLORS,
        title=f"3D PCA Dimensionality Reduction (Retaining {sum(exp_var):.2f}% of Total Variance)",
    )

    fig.update_traces(
        marker=dict(size=6, line=dict(width=0.5, color="white"), opacity=0.9)
    )

    fig.update_layout(
        template="plotly_white",
        scene=dict(
            xaxis_title=f"PC1 ({exp_var[0]:.1f}%)",
            yaxis_title=f"PC2 ({exp_var[1]:.1f}%)",
            zaxis_title=f"PC3 ({exp_var[2]:.1f}%)",
        ),
        height=620,
    )

    return fig, exp_var


def create_elbow_plot(df_eval):
    """
    Generate Elbow method curve and evaluation metrics using Plotly.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_eval["K"],
        y=df_eval["WCSS_or_L1Cost"],
        mode="lines+markers",
        name="Clustering Cost (Inertia/L1)",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=9, color="#1e40af"),
    ))

    fig.update_layout(
        template="plotly_white",
        title="Elbow Method Curve (Within-Cluster Cost vs Number of Clusters K)",
        xaxis_title="Number of Clusters (K)",
        yaxis_title="Within-Cluster Objective Cost",
        xaxis=dict(tickmode="linear", tick0=2, dtick=1),
        height=400,
    )
    return fig


def create_metrics_comparison_plot(df_eval):
    """
    Generate dual-axis or side-by-side bar chart of Silhouette Score and Davies-Bouldin.
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_eval["K"].astype(str),
        y=df_eval["Silhouette_Score"],
        name="Silhouette Score (Higher = Better)",
        marker_color="#10b981",
    ))

    fig.add_trace(go.Bar(
        x=df_eval["K"].astype(str),
        y=df_eval["Davies_Bouldin_Index"],
        name="Davies-Bouldin Index (Lower = Better)",
        marker_color="#f59e0b",
    ))

    fig.update_layout(
        template="plotly_white",
        barmode="group",
        title="Clustering Validation Metrics across Candidate K Values",
        xaxis_title="Number of Clusters (K)",
        yaxis_title="Metric Score",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_cluster_size_bar(labels):
    """
    Bar chart showing number of states/UTs in each cluster.
    """
    s_counts = pd.Series(labels).value_counts().sort_index()
    df_counts = pd.DataFrame({
        "Cluster": [f"Cluster {c}" for c in s_counts.index],
        "Count": s_counts.values
    })

    fig = px.bar(
        df_counts,
        x="Cluster",
        y="Count",
        color="Cluster",
        text="Count",
        color_discrete_sequence=CLUSTER_COLORS,
        title="Regional Cluster Membership Distribution",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(template="plotly_white", showlegend=False, height=350, yaxis_title="Number of States / UTs")
    return fig


def create_cluster_radar_profile(df_features_unscaled, labels, topics):
    """
    Radar chart comparing seasonal topic patterns across clusters.
    """
    df_temp = df_features_unscaled.copy()
    df_temp["cluster"] = labels

    cluster_means = df_temp.groupby("cluster").mean()
    fig = go.Figure()

    # Quarterly indicators across topics
    categories = []
    for t in topics:
        clean_t = t.replace(" ", "").replace("_", "")
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            col = f"{clean_t}_{q}"
            if col in cluster_means.columns:
                categories.append(col)

    # Pick top representative seasonal features to avoid radar clutter
    sample_categories = categories[:12] if len(categories) > 12 else categories

    for c_id in cluster_means.index:
        values = cluster_means.loc[c_id, sample_categories].values.tolist()
        values.append(values[0])  # Close the radar loop

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=sample_categories + [sample_categories[0]],
            fill="toself",
            name=f"Cluster {c_id}",
            line_color=CLUSTER_COLORS[c_id % len(CLUSTER_COLORS)],
            opacity=0.6,
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[-1.5, 2.0])),
        template="plotly_white",
        title="Standardized Seasonal Profile Across Clusters (Selected Seasonal Features)",
        height=520,
    )
    return fig

