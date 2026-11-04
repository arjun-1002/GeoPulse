"""
Clustering Module for Regional Tourism Demand Segmentation
==========================================================
Implements two distinct unsupervised clustering algorithms:
1. K-Means (Euclidean distance, arithmetic mean centroids, n_init=50)
2. K-Medians (Manhattan distance, coordinate-wise median centroids)
Includes multi-metric validation (WCSS / L1 Cost, Silhouette, Davies-Bouldin)
and stability evaluation using Adjusted Rand Index (ARI).
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, pairwise_distances, adjusted_rand_score


class KMediansManhattan:
    """
    K-Medians Clustering using Manhattan Distance (L1 norm).
    
    Academic Differentiation:
    -------------------------
    Standard K-Means defines the centroid as the arithmetic mean, which mathematically
    minimizes squared Euclidean distance (L2 norm).
    In contrast, K-Medians minimizes the sum of absolute Manhattan deviations (L1 norm)
    by computing the coordinate-wise median of cluster members.
    """
    def __init__(self, n_clusters=3, max_iter=300, random_state=42, n_init=10):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.n_init = n_init
        self.cluster_centers_ = None
        self.labels_ = None
        self.total_cost_ = None

    def fit_predict(self, X):
        X = np.asarray(X, dtype=np.float64)
        n_samples, n_features = X.shape

        best_cost = np.inf
        best_labels = None
        best_centers = None

        rng = np.random.RandomState(self.random_state)

        for init_idx in range(self.n_init):
            # Initialize centers by randomly sampling points
            initial_indices = rng.choice(n_samples, size=self.n_clusters, replace=False)
            centers = X[initial_indices].copy()

            for _ in range(self.max_iter):
                # Compute pairwise Manhattan distances: shape (n_samples, n_clusters)
                # d_ij = sum(|x_ik - c_jk|)
                distances = pairwise_distances(X, centers, metric="manhattan")
                labels = np.argmin(distances, axis=1)

                new_centers = np.empty_like(centers)
                for k in range(self.n_clusters):
                    members = X[labels == k]
                    if len(members) == 0:
                        # Reinitialize empty cluster to random sample
                        new_centers[k] = X[rng.choice(n_samples)]
                    else:
                        # Coordinate-wise median minimizes L1 distance
                        new_centers[k] = np.median(members, axis=0)

                # Convergence check
                if np.allclose(centers, new_centers, atol=1e-5):
                    break
                centers = new_centers

            # Calculate total Manhattan cost for this run
            distances = pairwise_distances(X, centers, metric="manhattan")
            labels = np.argmin(distances, axis=1)
            cost = float(np.sum(np.min(distances, axis=1)))

            if cost < best_cost:
                best_cost = cost
                best_labels = labels
                best_centers = centers

        self.cluster_centers_ = best_centers
        self.labels_ = best_labels
        self.total_cost_ = best_cost
        return best_labels


def evaluate_kmeans_models(X, k_range=range(2, 6), random_state=42, n_init=50):
    """
    Run K-Means across candidate K values and compute validation metrics.
    """
    records = []
    models = {}

    for k in k_range:
        if k >= len(X):
            continue
        km = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
        labels = km.fit_predict(X)

        wcss = km.inertia_
        sil = silhouette_score(X, labels, metric="euclidean")
        db = davies_bouldin_score(X, labels)

        records.append({
            "K": k,
            "Algorithm": "K-Means (Euclidean L2)",
            "WCSS_or_L1Cost": round(float(wcss), 2),
            "Silhouette_Score": round(float(sil), 4),
            "Davies_Bouldin_Index": round(float(db), 4),
        })
        models[k] = km

    df_eval = pd.DataFrame(records)
    return df_eval, models


def evaluate_kmedians_models(X, k_range=range(2, 6), random_state=42, n_init=10):
    """
    Run K-Medians (Manhattan distance) across candidate K values.
    """
    records = []
    models = {}

    for k in k_range:
        if k >= len(X):
            continue
        kmed = KMediansManhattan(n_clusters=k, random_state=random_state, n_init=n_init)
        labels = kmed.fit_predict(X)

        l1_cost = kmed.total_cost_
        sil = silhouette_score(X, labels, metric="manhattan")
        # Davies-Bouldin is defined for Euclidean, but we report it for consistency
        db = davies_bouldin_score(X, labels)

        records.append({
            "K": k,
            "Algorithm": "K-Medians (Manhattan L1)",
            "WCSS_or_L1Cost": round(float(l1_cost), 2),
            "Silhouette_Score": round(float(sil), 4),
            "Davies_Bouldin_Index": round(float(db), 4),
        })
        models[k] = kmed

    df_eval = pd.DataFrame(records)
    return df_eval, models


def run_clustering(X, algorithm="K-Means", k=3, random_state=42):
    """
    Execute selected clustering algorithm for a specific K.
    """
    if algorithm == "K-Means":
        model = KMeans(n_clusters=k, random_state=random_state, n_init=50)
        labels = model.fit_predict(X)
        metric_cost = model.inertia_
        sil = silhouette_score(X, labels, metric="euclidean")
        db = davies_bouldin_score(X, labels)
    else:  # K-Medians
        model = KMediansManhattan(n_clusters=k, random_state=random_state, n_init=15)
        labels = model.fit_predict(X)
        metric_cost = model.total_cost_
        sil = silhouette_score(X, labels, metric="manhattan")
        db = davies_bouldin_score(X, labels)

    metrics = {
        "algorithm": algorithm,
        "k": k,
        "cost": round(float(metric_cost), 2),
        "silhouette": round(float(sil), 4),
        "davies_bouldin": round(float(db), 4),
    }

    return labels, model, metrics


def assess_cluster_stability(X, algorithm="K-Means", k=3, seeds=(0, 7, 13, 21, 42, 77, 99, 123, 555, 999)):
    """
    Assess stability across multiple random seeds using Adjusted Rand Index.
    """
    clusterings = []
    for s in seeds:
        if algorithm == "K-Means":
            km = KMeans(n_clusters=k, random_state=s, n_init=10)
            clusterings.append(km.fit_predict(X))
        else:
            kmed = KMediansManhattan(n_clusters=k, random_state=s, n_init=5)
            clusterings.append(kmed.fit_predict(X))

    ari_values = []
    pairwise_records = []
    n = len(seeds)
    for i in range(n):
        for j in range(i + 1, n):
            ari = adjusted_rand_score(clusterings[i], clusterings[j])
            ari_values.append(ari)
            pairwise_records.append({
                "Seed_A": seeds[i],
                "Seed_B": seeds[j],
                "ARI": round(float(ari), 4)
            })

    mean_ari = float(np.mean(ari_values)) if ari_values else 1.0
    return mean_ari, pd.DataFrame(pairwise_records)

