"""
Clustering Module for Regional Search-Interest Analysis
======================================================

Project: CSE396 Unsupervised Learning Project
Stage: Day 3 (Experiments, Validation & PCA) & Day 4 (Profiling & Stability Analysis)

Description:
------------
This module implements the complete unsupervised learning lifecycle:
1. K-Means clustering across candidate cluster counts (K = 2, 3, 4, 5).
2. Calculation of cluster validation metrics:
   - Within-Cluster Sum of Squares (WCSS / Inertia)
   - Silhouette Score
   - Davies-Bouldin Index
3. Mathematically rigorous distance comparison:
   - Discusses Euclidean geometry in standard K-Means.
   - Implements K-Medoids (PAM) with Manhattan (L1) distance for valid comparison.
4. Principal Component Analysis (PCA) for 2D dimensionality reduction and visualization.
5. Day 4 Extensions:
   - Detailed cluster profiling (raw and standardized feature averages).
   - Identification of distinguishing high and low search topics per cluster.
   - Grounded, non-stereotyping cluster naming.
   - Cluster stability evaluation across multiple random seeds using Adjusted Rand Index (ARI).
6. Exports evaluation tables, profiles, and stability metrics to `outputs/results/`.
"""

import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, pairwise_distances, adjusted_rand_score
from sklearn.decomposition import PCA


def get_default_paths():
    """Resolve portable relative paths based on project structure."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scaled_data_path = os.path.join(base_dir, "data", "processed", "features_scaled.csv")
    raw_data_path = os.path.join(base_dir, "data", "raw", "google_trends_raw_india.csv")
    results_dir = os.path.join(base_dir, "outputs", "results")
    figures_dir = os.path.join(base_dir, "outputs", "figures")
    return scaled_data_path, raw_data_path, results_dir, figures_dir


def load_scaled_data(filepath=None):
    """Load standardized clustering feature matrix."""
    if filepath is None:
        filepath, _, _, _ = get_default_paths()

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Scaled feature file not found at: {filepath}")

    df_scaled = pd.read_csv(filepath, index_col=0)
    print(f"[CLUSTERING] Scaled data loaded successfully. Shape: {df_scaled.shape}")
    return df_scaled


def load_raw_data(filepath=None):
    """Load raw Google Trends dataset."""
    if filepath is None:
        _, filepath, _, _ = get_default_paths()

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw data file not found at: {filepath}")

    df_raw = pd.read_csv(filepath)
    return df_raw


def run_kmeans_experiments(X, k_values=(2, 3, 4, 5), random_state=42):
    """
    Apply K-Means clustering across specified values of K.

    Parameters:
    -----------
    X : np.ndarray or pd.DataFrame
        Standardized feature matrix.
    k_values : iterable of int
        Cluster counts to evaluate (default: 2, 3, 4, 5).
    random_state : int
        Seed for deterministic centroid initialization.

    Returns:
    --------
    tuple (pd.DataFrame, dict)
        metrics_df : Summary evaluation table (K, WCSS, Silhouette, Davies-Bouldin).
        models_dict : Dictionary of fitted KMeans model instances.
    """
    metrics_records = []
    models_dict = {}

    for k in k_values:
        km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = km.fit_predict(X)
        wcss = km.inertia_
        sil = silhouette_score(X, labels, metric="euclidean")
        db = davies_bouldin_score(X, labels)

        metrics_records.append({
            "K": k,
            "WCSS": round(float(wcss), 2),
            "Silhouette_Score": round(float(sil), 4),
            "Davies_Bouldin_Score": round(float(db), 4),
        })
        models_dict[k] = km

    metrics_df = pd.DataFrame(metrics_records)
    print("\n[VALIDATION] K-Means Clustering Validation Summary:")
    print(metrics_df.to_string(index=False))
    return metrics_df, models_dict


def run_kmedoids_manhattan(X, k_values=(2, 3, 4, 5), random_state=42, max_iter=100):
    """
    Implements Partitioning Around Medoids (PAM / K-Medoids) with Manhattan distance.

    Parameters:
    -----------
    X : np.ndarray
    k_values : iterable of int
    random_state : int
    max_iter : int

    Returns:
    --------
    tuple (pd.DataFrame, dict)
    """
    rng = np.random.RandomState(random_state)
    n_samples = X.shape[0]
    D = pairwise_distances(X, metric="manhattan")

    records = []
    medoids_dict = {}

    for k in k_values:
        medoids = rng.choice(n_samples, size=k, replace=False)

        for _ in range(max_iter):
            labels = np.argmin(D[:, medoids], axis=1)
            new_medoids = medoids.copy()
            for cluster_id in range(k):
                members = np.where(labels == cluster_id)[0]
                if len(members) == 0:
                    continue
                sub_D = D[np.ix_(members, members)]
                best_member = members[np.argmin(np.sum(sub_D, axis=1))]
                new_medoids[cluster_id] = best_member

            if np.array_equal(new_medoids, medoids):
                break
            medoids = new_medoids

        labels = np.argmin(D[:, medoids], axis=1)
        sil = silhouette_score(X, labels, metric="manhattan")
        total_cost = sum(np.min(D[:, medoids], axis=1))

        records.append({
            "K": k,
            "Total_Manhattan_Cost": round(float(total_cost), 2),
            "Silhouette_Score_Manhattan": round(float(sil), 4),
        })
        medoids_dict[k] = {"medoids": medoids, "labels": labels}

    kmedoids_df = pd.DataFrame(records)
    return kmedoids_df, medoids_dict


def compute_pca(X, n_components=2, random_state=42):
    """Apply Principal Component Analysis (PCA) to project data into 2D space."""
    pca = PCA(n_components=n_components, random_state=random_state)
    X_pca = pca.fit_transform(X)

    exp_var = pca.explained_variance_ratio_
    variance_df = pd.DataFrame({
        "Component": [f"PC{i+1}" for i in range(n_components)],
        "Explained_Variance_Ratio": [round(float(v), 4) for v in exp_var],
        "Explained_Variance_Percentage": [f"{v*100:.2f}%" for v in exp_var],
    })

    return X_pca, pca, variance_df


# ==========================================
# DAY 4: CLUSTER PROFILING & STABILITY
# ==========================================

CLUSTER_DESCRIPTIVE_NAMES = {
    0: "Cluster 0: High-Intensity Technology Innovation Hubs",
    1: "Cluster 1: Moderate / Balanced Applied-Technology Demand Regions",
    2: "Cluster 2: Emerging Digital Demand Regions with Consumer-AI Orientation",
}


def compute_cluster_profiles(df_raw, df_scaled, labels):
    """
    Compute raw and standardized topic averages for each cluster and identify high/low topics.

    Parameters:
    -----------
    df_raw : pd.DataFrame
        Raw dataset containing 'state' and 8 topic columns.
    df_scaled : pd.DataFrame
        Standardized features matrix.
    labels : np.ndarray
        Final cluster labels (for K=3).

    Returns:
    --------
    tuple (pd.DataFrame, pd.DataFrame, pd.DataFrame)
        df_profile_raw    : Raw average search indices (0-100) per cluster.
        df_profile_scaled : Z-score topic averages per cluster.
        df_regions_list   : Mapping of regions to clusters with descriptive names.
    """
    topic_cols = [c for c in df_raw.columns if c not in ["state", "geo_code", "cluster"]]

    df_raw_clustered = df_raw.copy()
    df_raw_clustered["cluster"] = labels

    df_scaled_clustered = df_scaled.copy()
    df_scaled_clustered["cluster"] = labels

    # 1. Raw averages per cluster
    df_profile_raw = df_raw_clustered.groupby("cluster")[topic_cols].mean().round(2)
    df_profile_raw["region_count"] = df_raw_clustered.groupby("cluster")["state"].count()
    df_profile_raw["cluster_name"] = [CLUSTER_DESCRIPTIVE_NAMES[c] for c in df_profile_raw.index]

    # 2. Scaled z-score averages per cluster
    df_profile_scaled = df_scaled_clustered.groupby("cluster")[topic_cols].mean().round(3)
    df_profile_scaled["region_count"] = df_raw_clustered.groupby("cluster")["state"].count()
    df_profile_scaled["cluster_name"] = [CLUSTER_DESCRIPTIVE_NAMES[c] for c in df_profile_scaled.index]

    # 3. Mapping of states to clusters
    regions_records = []
    for c_id in sorted(df_raw_clustered["cluster"].unique()):
        sub_states = df_raw_clustered[df_raw_clustered["cluster"] == c_id]["state"].tolist()
        for s in sub_states:
            regions_records.append({
                "state": s,
                "cluster": c_id,
                "cluster_name": CLUSTER_DESCRIPTIVE_NAMES[c_id],
            })
    df_regions_list = pd.DataFrame(regions_records)

    print("\n[PROFILING] Cluster Feature Averages (Raw Google Trends Index 0-100):")
    print(df_profile_raw[topic_cols + ["region_count"]])

    print("\n[PROFILING] Cluster Feature Averages (Standardized Z-Scores):")
    print(df_profile_scaled[topic_cols + ["region_count"]])

    return df_profile_raw, df_profile_scaled, df_regions_list


def compute_clustering_stability(X, k=3, seeds=(0, 7, 13, 21, 42, 77, 99, 123, 555, 999)):
    """
    Assess clustering stability across multiple random centroid initializations using Adjusted Rand Index.

    Parameters:
    -----------
    X : np.ndarray
        Standardized feature matrix.
    k : int
        Number of clusters (default: 3).
    seeds : tuple of int
        Random seeds to test.

    Returns:
    --------
    tuple (float, pd.DataFrame)
        mean_ari : Mean pairwise Adjusted Rand Index.
        df_stability : Table of pairwise ARI comparisons.
    """
    clusterings = []
    for s in seeds:
        km = KMeans(n_clusters=k, random_state=s, n_init=10)
        clusterings.append(km.fit_predict(X))

    ari_records = []
    ari_values = []
    for i in range(len(seeds)):
        for j in range(i + 1, len(seeds)):
            ari = adjusted_rand_score(clusterings[i], clusterings[j])
            ari_values.append(ari)
            ari_records.append({
                "Seed_A": seeds[i],
                "Seed_B": seeds[j],
                "Adjusted_Rand_Index": round(float(ari), 4),
            })

    df_stability = pd.DataFrame(ari_records)
    mean_ari = float(np.mean(ari_values))

    print(f"\n[STABILITY] Cluster Stability Evaluation across {len(seeds)} Random Seeds:")
    print(f"  Mean Adjusted Rand Index (ARI): {mean_ari:.4f}")
    print(f"  Minimum ARI: {np.min(ari_values):.4f}, Maximum ARI: {np.max(ari_values):.4f}")
    if mean_ari >= 0.90:
        print("  Interpretation: Exceptionally high stability. Cluster boundaries are highly robust to initialization.")
    elif mean_ari >= 0.75:
        print("  Interpretation: Good stability with minor boundary shifts.")
    else:
        print("  Interpretation: Moderate to low stability; clusters are sensitive to seed selection.")

    return mean_ari, df_stability


def export_all_results(
    metrics_df,
    distance_df,
    df_scaled,
    models_dict,
    X_pca,
    df_profile_raw,
    df_profile_scaled,
    df_regions_list,
    df_stability,
    results_dir=None,
):
    """Export all tables and results across Day 3 and Day 4."""
    if results_dir is None:
        _, _, results_dir, _ = get_default_paths()

    os.makedirs(results_dir, exist_ok=True)

    # Day 3 files
    metrics_df.to_csv(os.path.join(results_dir, "clustering_evaluation_metrics.csv"), index=False)
    distance_df.to_csv(os.path.join(results_dir, "distance_comparison_metrics.csv"), index=False)

    assignments_df = pd.DataFrame(index=df_scaled.index)
    assignments_df.index.name = "state"
    for k, model in models_dict.items():
        assignments_df[f"cluster_k{k}"] = model.labels_
    assignments_df["final_cluster_name"] = [CLUSTER_DESCRIPTIVE_NAMES[c] for c in models_dict[3].labels_]
    assignments_df.to_csv(os.path.join(results_dir, "cluster_assignments.csv"))

    pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"], index=df_scaled.index)
    pca_df["cluster_k3"] = models_dict[3].labels_
    pca_df.to_csv(os.path.join(results_dir, "pca_transformed_data.csv"))

    # Day 4 files
    df_profile_raw.to_csv(os.path.join(results_dir, "cluster_profiles_raw.csv"))
    df_profile_scaled.to_csv(os.path.join(results_dir, "cluster_profiles_scaled.csv"))
    df_regions_list.to_csv(os.path.join(results_dir, "cluster_regions_listing.csv"), index=False)
    df_stability.to_csv(os.path.join(results_dir, "stability_analysis_ari.csv"), index=False)

    print(f"\n[EXPORT] All Day 3 & Day 4 tables successfully exported to: {results_dir}")


def run_full_pipeline():
    """Run full unsupervised clustering pipeline from data load to stability analysis."""
    print("=" * 70)
    print("CSE396 - Full Clustering Pipeline (Day 3 + Day 4)")
    print("=" * 70)

    df_scaled = load_scaled_data()
    df_raw = load_raw_data()
    X = df_scaled.values

    # K-Means experiments
    metrics_df, models_dict = run_kmeans_experiments(X)

    # Manhattan experiment
    distance_df, medoids_dict = run_kmedoids_manhattan(X)

    # PCA
    X_pca, pca_model, variance_df = compute_pca(X)

    # Day 4: Profiling & Stability
    final_labels = models_dict[3].labels_
    df_profile_raw, df_profile_scaled, df_regions_list = compute_cluster_profiles(
        df_raw, df_scaled, final_labels
    )
    mean_ari, df_stability = compute_clustering_stability(X, k=3)

    # Export
    export_all_results(
        metrics_df,
        distance_df,
        df_scaled,
        models_dict,
        X_pca,
        df_profile_raw,
        df_profile_scaled,
        df_regions_list,
        df_stability,
    )

    return {
        "metrics_df": metrics_df,
        "df_profile_raw": df_profile_raw,
        "df_profile_scaled": df_profile_scaled,
        "df_regions_list": df_regions_list,
        "df_stability": df_stability,
        "mean_ari": mean_ari,
        "models_dict": models_dict,
        "X_pca": X_pca,
        "pca_model": pca_model,
    }


if __name__ == "__main__":
    results = run_full_pipeline()
