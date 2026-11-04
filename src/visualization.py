"""
Visualization Module for Regional Search-Interest Clustering
============================================================

Project: CSE396 Unsupervised Learning Project
Stage: Day 2 (EDA), Day 3 (Validation & PCA), Day 4 (Cluster Profiles & Comparison)

Description:
------------
This module produces clean, publication-ready figures for the entire project:
Day 2:
1. Topic Search-Interest Distributions (Box plots / Histograms)
2. State-level Technology Interest Comparison (Top 15 States)
3. Topic Correlation Heatmap
Day 3:
4. Elbow Method (WCSS / Inertia) & Multi-Metric Validation (Silhouette, Davies-Bouldin)
5. 2D PCA Cluster Scatter Plot with Centroids, State Annotations & Explained Variance
6. Distance Metric Geometry Comparison (Euclidean K-Means vs Manhattan K-Medoids)
Day 4:
7. Cluster Profile Standardized Z-Score Heatmap
8. Comparative Topic Search-Interest Grouped Bar Chart by Cluster
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set consistent styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10


# ==========================================
# DAY 2 EDA VISUALIZATIONS
# ==========================================

def plot_topic_distributions(df_features, save_path=None):
    """Plot boxplots and distributions for each of the 8 technology topics."""
    fig, axes = plt.subplots(2, 4, figsize=(16, 8), sharey=True)
    axes = axes.flatten()

    palette = sns.color_palette("mako", n_colors=len(df_features.columns))

    for idx, col in enumerate(df_features.columns):
        clean_title = col.replace("_", " ").title()
        sns.boxplot(
            y=df_features[col],
            ax=axes[idx],
            color=palette[idx],
            width=0.4,
            boxprops=dict(alpha=0.7),
        )
        sns.stripplot(
            y=df_features[col],
            ax=axes[idx],
            color="black",
            size=4,
            jitter=0.2,
            alpha=0.6,
        )
        axes[idx].set_title(clean_title, fontweight="bold")
        axes[idx].set_ylabel("Search Interest Index (0–100)" if idx % 4 == 0 else "")
        axes[idx].set_ylim(-5, 105)

    plt.suptitle(
        "Regional Search-Interest Distributions Across 36 Indian States/UTs\n(Google Trends, Past 12 Months)",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[FIGURE] Saved topic distributions to: {save_path}")

    return fig


def plot_state_comparison(df_combined, top_n=15, save_path=None):
    """Plot top N Indian States/UTs by mean technology search interest."""
    topic_cols = [
        "artificial_intelligence",
        "machine_learning",
        "data_science",
        "cloud_computing",
        "cybersecurity",
        "blockchain",
        "internet_of_things",
        "chatgpt",
    ]

    df_rank = df_combined.copy()
    df_rank["mean_search_index"] = df_rank[topic_cols].mean(axis=1)
    df_top = df_rank.sort_values(by="mean_search_index", ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = sns.barplot(
        x="mean_search_index",
        y="state",
        data=df_top,
        palette="viridis",
        ax=ax,
        hue="state",
        legend=False,
    )

    for bar in bars.patches:
        width = bar.get_width()
        ax.annotate(
            f"{width:.1f}",
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(5, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_title(
        f"Top {top_n} Indian States/UTs by Overall Average Search Interest Across Selected Technologies",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Mean Search Interest Index (Across 8 Topics, 0–100)", fontweight="bold")
    ax.set_ylabel("State / Union Territory", fontweight="bold")
    ax.set_xlim(0, 100)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[FIGURE] Saved state comparison barplot to: {save_path}")

    return fig


def plot_correlation_heatmap(df_features, save_path=None):
    """Plot correlation matrix heatmap among the 8 technology topics."""
    corr = df_features.corr()
    clean_labels = [c.replace("_", " ").title() for c in corr.columns]

    fig, ax = plt.subplots(figsize=(9, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-0.2,
        vmax=1.0,
        square=True,
        linewidths=0.8,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation (r)"},
        xticklabels=clean_labels,
        yticklabels=clean_labels,
        ax=ax,
    )

    ax.set_title(
        "Inter-Topic Pearson Correlation Matrix\n(Regional Search Demand Patterns Across India)",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[FIGURE] Saved correlation heatmap to: {save_path}")

    return fig


# ==========================================
# DAY 3 CLUSTERING & VALIDATION VISUALIZATIONS
# ==========================================

def plot_elbow_and_metrics(metrics_df, save_path=None):
    """Plot the Elbow Method (WCSS / Inertia) alongside Silhouette and Davies-Bouldin metrics."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    k_vals = metrics_df["K"]

    # 1. Elbow Method (WCSS / Inertia)
    axes[0].plot(k_vals, metrics_df["WCSS"], marker="o", color="#1f77b4", linewidth=2.5, markersize=8)
    axes[0].set_title("Elbow Method (WCSS / Inertia)", fontweight="bold")
    axes[0].set_xlabel("Number of Clusters (K)", fontweight="bold")
    axes[0].set_ylabel("Within-Cluster Sum of Squares (WCSS)", fontweight="bold")
    axes[0].set_xticks(k_vals)
    for k, w in zip(k_vals, metrics_df["WCSS"]):
        axes[0].annotate(f"{w:.1f}", (k, w), textcoords="offset points", xytext=(0, 10), ha="center", fontweight="bold")

    # 2. Silhouette Score (Higher is better)
    axes[1].plot(k_vals, metrics_df["Silhouette_Score"], marker="s", color="#2ca02c", linewidth=2.5, markersize=8)
    axes[1].set_title("Silhouette Analysis (Higher = Better Separation)", fontweight="bold")
    axes[1].set_xlabel("Number of Clusters (K)", fontweight="bold")
    axes[1].set_ylabel("Silhouette Score", fontweight="bold")
    axes[1].set_xticks(k_vals)
    axes[1].set_ylim(0.2, 0.6)
    for k, s in zip(k_vals, metrics_df["Silhouette_Score"]):
        axes[1].annotate(f"{s:.4f}", (k, s), textcoords="offset points", xytext=(0, 10), ha="center", fontweight="bold")

    # 3. Davies-Bouldin Score (Lower is better)
    axes[2].plot(k_vals, metrics_df["Davies_Bouldin_Score"], marker="^", color="#d62728", linewidth=2.5, markersize=8)
    axes[2].set_title("Davies-Bouldin Index (Lower = Better Partition)", fontweight="bold")
    axes[2].set_xlabel("Number of Clusters (K)", fontweight="bold")
    axes[2].set_ylabel("Davies-Bouldin Score", fontweight="bold")
    axes[2].set_xticks(k_vals)
    for k, db in zip(k_vals, metrics_df["Davies_Bouldin_Score"]):
        axes[2].annotate(f"{db:.4f}", (k, db), textcoords="offset points", xytext=(0, 10), ha="center", fontweight="bold")

    plt.suptitle(
        "K-Means Clustering Validation Metrics Across Candidate K Values (K = 2, 3, 4, 5)",
        fontsize=14,
        fontweight="bold",
        y=1.03,
    )
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[FIGURE] Saved Elbow & validation metrics to: {save_path}")

    return fig


def plot_pca_clusters(
    X_pca,
    labels,
    state_names,
    pca_model,
    k=3,
    centroids_pca=None,
    save_path=None,
):
    """Generate 2D PCA cluster scatter plot with centroids and region annotations."""
    fig, ax = plt.subplots(figsize=(13, 8))

    exp_var = pca_model.explained_variance_ratio_ * 100
    palette = sns.color_palette("tab10", n_colors=k)

    for cluster_id in range(k):
        mask = (labels == cluster_id)
        ax.scatter(
            X_pca[mask, 0],
            X_pca[mask, 1],
            s=120,
            color=palette[cluster_id],
            label=f"Cluster {cluster_id} (n={sum(mask)})",
            alpha=0.85,
            edgecolors="black",
            linewidth=1.2,
        )

    if centroids_pca is not None:
        ax.scatter(
            centroids_pca[:, 0],
            centroids_pca[:, 1],
            s=250,
            marker="X",
            color="red",
            edgecolors="black",
            linewidth=2,
            label="Cluster Centroids (Projected)",
            zorder=10,
        )

    highlight_states = [
        "Karnataka", "Maharashtra", "Telangana", "Delhi", "Andhra Pradesh",
        "Tamil Nadu", "Bihar", "Uttar Pradesh", "Assam", "Kerala", "Gujarat",
        "Andaman and Nicobar Islands"
    ]

    for i, state in enumerate(state_names):
        if state in highlight_states:
            ax.annotate(
                state,
                xy=(X_pca[i, 0], X_pca[i, 1]),
                xytext=(6, 5),
                textcoords="offset points",
                fontsize=8.5,
                fontweight="semibold",
                alpha=0.9,
            )

    ax.set_title(
        f"2D PCA Projection of Regional Search Clusters (K={k})\n"
        f"Preserving {sum(exp_var):.2f}% of Multidimensional Variance Across India",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel(f"Principal Component 1 — PC1 ({exp_var[0]:.2f}% Variance Explained)", fontweight="bold")
    ax.set_ylabel(f"Principal Component 2 — PC2 ({exp_var[1]:.2f}% Variance Explained)", fontweight="bold")
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.axvline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.legend(frameon=True, facecolor="white", edgecolor="lightgray", loc="best")

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[FIGURE] Saved 2D PCA cluster visualization to: {save_path}")

    return fig


def plot_distance_comparison(
    kmeans_labels,
    kmedoids_labels,
    state_names,
    X_pca,
    save_path=None,
):
    """Compare Euclidean K-Means vs Manhattan K-Medoids cluster partitions."""
    fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)

    palette_km = sns.color_palette("tab10", n_colors=len(np.unique(kmeans_labels)))
    for c_id in np.unique(kmeans_labels):
        mask = (kmeans_labels == c_id)
        axes[0].scatter(
            X_pca[mask, 0],
            X_pca[mask, 1],
            s=100,
            color=palette_km[c_id],
            label=f"Cluster {c_id} (n={sum(mask)})",
            edgecolors="black",
            linewidth=1.0,
            alpha=0.8,
        )
    axes[0].set_title("Standard K-Means (Euclidean Geometry L2)", fontweight="bold")
    axes[0].set_xlabel("PC1", fontweight="bold")
    axes[0].set_ylabel("PC2", fontweight="bold")
    axes[0].legend(frameon=True)
    axes[0].axhline(0, color="gray", linestyle="--", alpha=0.4)
    axes[0].axvline(0, color="gray", linestyle="--", alpha=0.4)

    palette_pam = sns.color_palette("Set2", n_colors=len(np.unique(kmedoids_labels)))
    for c_id in np.unique(kmedoids_labels):
        mask = (kmedoids_labels == c_id)
        axes[1].scatter(
            X_pca[mask, 0],
            X_pca[mask, 1],
            s=100,
            color=palette_pam[c_id],
            label=f"Cluster {c_id} (n={sum(mask)})",
            edgecolors="black",
            linewidth=1.0,
            alpha=0.8,
        )
    axes[1].set_title("K-Medoids / PAM (Manhattan Distance L1)", fontweight="bold")
    axes[1].set_xlabel("PC1", fontweight="bold")
    axes[1].legend(frameon=True)
    axes[1].axhline(0, color="gray", linestyle="--", alpha=0.4)
    axes[1].axvline(0, color="gray", linestyle="--", alpha=0.4)

    plt.suptitle(
        "Distance Metric Comparison: Euclidean (L2) vs Manhattan (L1) Space\n"
        "(Evaluating Cluster Robustness Across Geometry Formulations)",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[FIGURE] Saved distance comparison figure to: {save_path}")

    return fig


# ==========================================
# DAY 4: CLUSTER PROFILE VISUALIZATIONS
# ==========================================

def plot_cluster_profile_heatmap(df_profile_scaled, save_path=None):
    """
    Plot heatmap of standardized (Z-Score) feature averages for each cluster.

    Parameters:
    -----------
    df_profile_scaled : pd.DataFrame
        Scaled topic means per cluster.
    save_path : str, optional
    """
    topic_cols = [
        "artificial_intelligence",
        "machine_learning",
        "data_science",
        "cloud_computing",
        "cybersecurity",
        "blockchain",
        "internet_of_things",
        "chatgpt",
    ]

    heatmap_data = df_profile_scaled[topic_cols].copy()
    clean_cols = [c.replace("_", " ").title() for c in topic_cols]
    heatmap_data.columns = clean_cols

    # Descriptive cluster row labels
    row_labels = [
        "Cluster 0: High-Intensity Tech Hubs (n=8)",
        "Cluster 1: Moderate / Balanced Demand (n=17)",
        "Cluster 2: Emerging Demand / Consumer-AI (n=11)",
    ]
    heatmap_data.index = row_labels

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt="+.2f",
        cmap="coolwarm",
        center=0.0,
        vmin=-1.5,
        vmax=1.8,
        cbar_kws={"label": "Standardized Search Intensity (Z-Score)"},
        linewidths=1.0,
        linecolor="white",
        ax=ax,
    )

    ax.set_title(
        "Cluster Profile Heatmap: Standardized Search Intensity by Technology Topic (K = 3)\n"
        "(Values show deviations above (+) or below (-) the national average)",
        fontsize=12,
        fontweight="bold",
        pad=15,
    )
    plt.xticks(rotation=30, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[FIGURE] Saved cluster profile heatmap to: {save_path}")

    return fig


def plot_cluster_topic_comparison(df_profile_raw, save_path=None):
    """
    Plot grouped bar chart comparing raw search interest indices (0-100) across clusters.

    Parameters:
    -----------
    df_profile_raw : pd.DataFrame
        Raw topic means per cluster.
    save_path : str, optional
    """
    topic_cols = [
        "artificial_intelligence",
        "machine_learning",
        "data_science",
        "cloud_computing",
        "cybersecurity",
        "blockchain",
        "internet_of_things",
        "chatgpt",
    ]

    clean_topics = [c.replace("_", " ").title() for c in topic_cols]

    # Reshape for seaborn grouped barplot
    data_list = []
    cluster_labels = [
        "Cluster 0: High-Intensity Hubs (n=8)",
        "Cluster 1: Moderate Demand (n=17)",
        "Cluster 2: Emerging Demand (n=11)",
    ]

    for c_id in range(len(df_profile_raw)):
        c_name = cluster_labels[c_id]
        for col, c_topic in zip(topic_cols, clean_topics):
            data_list.append({
                "Cluster": c_name,
                "Topic": c_topic,
                "Search_Index": df_profile_raw.loc[c_id, col],
            })

    df_plot = pd.DataFrame(data_list)

    fig, ax = plt.subplots(figsize=(15, 6))
    sns.barplot(
        data=df_plot,
        x="Topic",
        y="Search_Index",
        hue="Cluster",
        palette=["#2b5c8f", "#5b9279", "#d66853"],
        ax=ax,
    )

    ax.set_title(
        "Comparison of Emerging Technology Search Interest Across Discovered Clusters (0–100 Scale)",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Technology Domain", fontweight="bold")
    ax.set_ylabel("Average Google Trends Search Index (0–100)", fontweight="bold")
    ax.set_ylim(0, 105)
    plt.xticks(rotation=25, ha="right")
    ax.legend(title="Cluster Segment", frameon=True, loc="upper right")
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[FIGURE] Saved cluster topic comparison bar chart to: {save_path}")

    return fig


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    raw_csv = os.path.join(base_dir, "data", "raw", "google_trends_raw_india.csv")
    fig_dir = os.path.join(base_dir, "outputs", "figures")
    res_dir = os.path.join(base_dir, "outputs", "results")

    df = pd.read_csv(raw_csv)
    topic_cols = [c for c in df.columns if c not in ["state", "geo_code"]]

    # Day 2 Visualizations
    plot_topic_distributions(df[topic_cols], save_path=os.path.join(fig_dir, "topic_distributions.png"))
    plot_state_comparison(df, top_n=15, save_path=os.path.join(fig_dir, "state_tech_interest_comparison.png"))
    plot_correlation_heatmap(df[topic_cols], save_path=os.path.join(fig_dir, "topic_correlation_heatmap.png"))

    # Day 3 Visualizations
    scaled_csv = os.path.join(base_dir, "data", "processed", "features_scaled.csv")
    if os.path.exists(scaled_csv):
        from src.clustering import run_kmeans_experiments, run_kmedoids_manhattan, compute_pca
        df_scaled = pd.read_csv(scaled_csv, index_col=0)
        X = df_scaled.values
        state_names = df_scaled.index.tolist()

        metrics_df, models_dict = run_kmeans_experiments(X)
        distance_df, medoids_dict = run_kmedoids_manhattan(X)
        X_pca, pca_model, var_df = compute_pca(X)

        plot_elbow_and_metrics(metrics_df, save_path=os.path.join(fig_dir, "elbow_and_validation_metrics.png"))

        km3 = models_dict[3]
        centroids_pca = pca_model.transform(km3.cluster_centers_)
        plot_pca_clusters(
            X_pca, km3.labels_, state_names, pca_model, k=3,
            centroids_pca=centroids_pca, save_path=os.path.join(fig_dir, "pca_cluster_visualization.png")
        )

        plot_distance_comparison(
            km3.labels_, medoids_dict[3]["labels"], state_names, X_pca,
            save_path=os.path.join(fig_dir, "distance_metric_comparison.png")
        )

    # Day 4 Visualizations
    raw_prof_csv = os.path.join(res_dir, "cluster_profiles_raw.csv")
    scaled_prof_csv = os.path.join(res_dir, "cluster_profiles_scaled.csv")
    if os.path.exists(raw_prof_csv) and os.path.exists(scaled_prof_csv):
        df_prof_raw = pd.read_csv(raw_prof_csv, index_col=0)
        df_prof_scaled = pd.read_csv(scaled_prof_csv, index_col=0)

        plot_cluster_profile_heatmap(df_prof_scaled, save_path=os.path.join(fig_dir, "cluster_profile_heatmap.png"))
        plot_cluster_topic_comparison(df_prof_raw, save_path=os.path.join(fig_dir, "cluster_topic_comparison.png"))
