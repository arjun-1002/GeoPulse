"""
Visualization Module for Regional Search-Interest Clustering
============================================================

Project: CSE396 Unsupervised Learning Project
Stage: Day 2 — Exploratory Data Analysis & Diagnostic Plots

Description:
------------
This module produces clean, publication-ready figures for Exploratory Data Analysis (EDA):
1. Topic Search-Interest Distributions (Box plots / Histograms)
2. State-level Technology Interest Comparison (Top 15 States)
3. Topic Correlation Heatmap
"""

import os
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


def plot_topic_distributions(df_features, save_path=None):
    """
    Plot boxplots and distributions for each of the 8 technology topics.

    Parameters:
    -----------
    df_features : pd.DataFrame
        Unscaled numerical feature matrix.
    save_path : str, optional
        Path to save figure.
    """
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
    """
    Plot top N Indian States/UTs by mean technology search interest.

    Parameters:
    -----------
    df_combined : pd.DataFrame
        DataFrame with 'state' and 8 topic columns.
    top_n : int
        Number of top states to display.
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
    """
    Plot correlation matrix heatmap among the 8 technology topics.

    Parameters:
    -----------
    df_features : pd.DataFrame
        Topic feature matrix.
    save_path : str, optional
    """
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


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv = os.path.join(base_dir, "data", "raw", "google_trends_raw_india.csv")
    fig_dir = os.path.join(base_dir, "outputs", "figures")

    df = pd.read_csv(raw_csv)
    topic_cols = [c for c in df.columns if c not in ["state", "geo_code"]]

    plot_topic_distributions(df[topic_cols], save_path=os.path.join(fig_dir, "topic_distributions.png"))
    plot_state_comparison(df, top_n=15, save_path=os.path.join(fig_dir, "state_tech_interest_comparison.png"))
    plot_correlation_heatmap(df[topic_cols], save_path=os.path.join(fig_dir, "topic_correlation_heatmap.png"))
