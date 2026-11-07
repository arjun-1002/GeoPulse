
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

import os

data = pd.read_csv(
    "data/kerala_tourism_kmeans_input_10_destinations.csv"
)

destinations = data["Destination"]
features = data.drop(columns=["Destination"])

X = np.log1p(features)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

scores = []

for k in range(2, 6):
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    labels = model.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)

    scores.append({
        "Clusters": k,
        "Silhouette Score": score
    })

    print("K =", k, "Silhouette Score =", round(score, 3))

score_df = pd.DataFrame(scores)

best_k = int(
    score_df.loc[
        score_df["Silhouette Score"].idxmax(),
        "Clusters"
    ]
)

print("\nSelected number of clusters:", best_k)

final_model = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=20
)

data["Cluster"] = final_model.fit_predict(X_scaled)

os.makedirs("results", exist_ok=True)

data.to_csv(
    "results/destination_clusters.csv",
    index=False
)

summary = data.groupby("Cluster")[features.columns].mean()

summary.to_csv("results/cluster_summary.csv")

plt.figure(figsize=(8, 5))
plt.plot(
    score_df["Clusters"],
    score_df["Silhouette Score"],
    marker="o"
)
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.title("K-Means Cluster Evaluation")
plt.xticks(range(2, 6))
plt.grid(True)
plt.savefig("results/silhouette_scores.png")
plt.show()

pca = PCA(n_components=2)
reduced_data = pca.fit_transform(X_scaled)

plt.figure(figsize=(9, 6))
plt.scatter(
    reduced_data[:, 0],
    reduced_data[:, 1],
    c=data["Cluster"],
    cmap="viridis",
    s=100
)

for i, name in enumerate(destinations):
    plt.annotate(
        name,
        (reduced_data[i, 0], reduced_data[i, 1])
    )

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Kerala Tourism Destination Clusters")
plt.savefig("results/destination_clusters.png")
plt.show()

print("\nDestination Cluster Results:")
print(data[["Destination", "Cluster"]])

print("\nCluster Summary:")
print(summary)
