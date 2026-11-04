"""
CSE396 Interactive Web Application & Visual Dashboard
======================================================
Project Title: Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering
Author: Arjun (B.Tech CSE)

Description:
------------
This web application provides a modern, interactive, and user-friendly interface
for exploring the CSE396 Unsupervised Learning Project:
- Executive Overview & Problem Statement
- Interactive Exploratory Data Analysis
- K-Means Experiments, Elbow Method & Validation Tables
- Interactive 2D PCA Cluster Scatter Plot with State Tooltips
- Discovered Cluster Profiles with Heatmaps and Member Listings
- Interactive State-by-State Search Intensity & Radar Profile Analyzer
- Embedded Comprehensive Viva Voce Revision Guide (26 Questions)

Usage:
------
Run:
    python app.py
Open:
    http://127.0.0.1:8000 (Opens automatically in your browser)
"""

import os
import sys
import json
import webbrowser
import threading
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="CSE396 - Regional Search-Interest Clustering Dashboard",
    description="Interactive Web Interface for Unsupervised Regional Clustering in India",
    version="1.0.0",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(BASE_DIR, "outputs", "figures")
RESULTS_DIR = os.path.join(BASE_DIR, "outputs", "results")
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "google_trends_raw_india.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "google_trends_processed_india.csv")

# Mount figures directory for static image serving
if os.path.exists(FIGURES_DIR):
    app.mount("/figures", StaticFiles(directory=FIGURES_DIR), name="figures")

# Load precomputed datasets
def load_data():
    df_raw = pd.read_csv(RAW_DATA_PATH)
    df_metrics = pd.read_csv(os.path.join(RESULTS_DIR, "clustering_evaluation_metrics.csv"))
    df_assignments = pd.read_csv(os.path.join(RESULTS_DIR, "cluster_assignments.csv"))
    df_pca = pd.read_csv(os.path.join(RESULTS_DIR, "pca_transformed_data.csv"))
    df_prof_raw = pd.read_csv(os.path.join(RESULTS_DIR, "cluster_profiles_raw.csv"), index_col=0)
    df_prof_scaled = pd.read_csv(os.path.join(RESULTS_DIR, "cluster_profiles_scaled.csv"), index_col=0)
    df_regions = pd.read_csv(os.path.join(RESULTS_DIR, "cluster_regions_listing.csv"))
    df_stability = pd.read_csv(os.path.join(RESULTS_DIR, "stability_analysis_ari.csv"))
    return {
        "raw": df_raw,
        "metrics": df_metrics,
        "assignments": df_assignments,
        "pca": df_pca,
        "prof_raw": df_prof_raw,
        "prof_scaled": df_prof_scaled,
        "regions": df_regions,
        "stability": df_stability,
    }

DATA = load_data()
TOPIC_COLS = [c for c in DATA["raw"].columns if c not in ["state", "geo_code"]]
TOPIC_NAMES = [c.replace("_", " ").title() for c in TOPIC_COLS]

CLUSTER_NAMES = {
    0: "High-Intensity Technology Innovation Hubs",
    1: "Moderate / Balanced Applied-Technology Demand",
    2: "Emerging Digital Demand Regions (Consumer-AI)",
}

CLUSTER_COLORS = {
    0: "#2563eb",  # Blue
    1: "#10b981",  # Emerald Green
    2: "#f59e0b",  # Amber / Coral
}


# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.get("/api/summary")
def get_summary():
    """Return high-level executive statistics."""
    mean_ari = float(DATA["stability"]["Adjusted_Rand_Index"].mean())
    return {
        "total_regions": int(len(DATA["raw"])),
        "total_topics": len(TOPIC_COLS),
        "topics": TOPIC_NAMES,
        "optimal_k": 3,
        "pca_variance": 89.33,
        "mean_ari": round(mean_ari, 4),
        "cluster_counts": DATA["regions"]["cluster"].value_counts().to_dict(),
    }


@app.get("/api/metrics")
def get_metrics():
    """Return K-Means validation table."""
    return DATA["metrics"].to_dict(orient="records")


@app.get("/api/pca_data")
def get_pca_data():
    """Return 2D PCA coordinates with state metadata and cluster assignments."""
    records = []
    for _, row in DATA["pca"].iterrows():
        state = row["state"]
        c_id = int(row["cluster_k3"])
        raw_row = DATA["raw"][DATA["raw"]["state"] == state].iloc[0]
        records.append({
            "state": state,
            "pc1": round(float(row["PC1"]), 3),
            "pc2": round(float(row["PC2"]), 3),
            "cluster": c_id,
            "cluster_name": CLUSTER_NAMES.get(c_id, f"Cluster {c_id}"),
            "color": CLUSTER_COLORS.get(c_id, "#6b7280"),
            "topics": {col: int(raw_row[col]) for col in TOPIC_COLS},
        })
    return records


@app.get("/api/cluster_profiles")
def get_cluster_profiles():
    """Return raw and scaled cluster topic averages."""
    raw_dict = DATA["prof_raw"].to_dict(orient="index")
    scaled_dict = DATA["prof_scaled"].to_dict(orient="index")
    output = []
    for c_id in sorted(raw_dict.keys()):
        output.append({
            "cluster": c_id,
            "cluster_name": CLUSTER_NAMES.get(c_id, f"Cluster {c_id}"),
            "color": CLUSTER_COLORS.get(c_id, "#6b7280"),
            "region_count": int(raw_dict[c_id].get("region_count", 0)),
            "raw_averages": {col: round(float(raw_dict[c_id][col]), 1) for col in TOPIC_COLS},
            "scaled_averages": {col: round(float(scaled_dict[c_id][col]), 2) for col in TOPIC_COLS},
            "member_states": DATA["regions"][DATA["regions"]["cluster"] == c_id]["state"].tolist(),
        })
    return output


@app.get("/api/states")
def get_all_states():
    """Return all 36 Indian states with their topic values and cluster."""
    output = []
    for _, row in DATA["raw"].iterrows():
        state = row["state"]
        assign_row = DATA["assignments"][DATA["assignments"]["state"] == state].iloc[0]
        c_id = int(assign_row["cluster_k3"])
        output.append({
            "state": state,
            "geo_code": row["geo_code"],
            "cluster": c_id,
            "cluster_name": CLUSTER_NAMES.get(c_id, f"Cluster {c_id}"),
            "color": CLUSTER_COLORS.get(c_id, "#6b7280"),
            "topics": {col: int(row[col]) for col in TOPIC_COLS},
            "mean_index": round(float(row[TOPIC_COLS].mean()), 1),
        })
    output.sort(key=lambda x: x["mean_index"], reverse=True)
    return output


@app.get("/api/state/{state_name}")
def get_state_detail(state_name: str):
    """Return individual state profile compared with its cluster average and national average."""
    matched = DATA["raw"][DATA["raw"]["state"].str.lower() == state_name.lower()]
    if matched.empty:
        raise HTTPException(status_code=404, detail="State not found")
    
    row = matched.iloc[0]
    assign_row = DATA["assignments"][DATA["assignments"]["state"] == row["state"]].iloc[0]
    c_id = int(assign_row["cluster_k3"])
    national_means = DATA["raw"][TOPIC_COLS].mean().round(1).to_dict()
    cluster_means = DATA["prof_raw"].loc[c_id, TOPIC_COLS].round(1).to_dict()

    return {
        "state": row["state"],
        "geo_code": row["geo_code"],
        "cluster": c_id,
        "cluster_name": CLUSTER_NAMES.get(c_id, f"Cluster {c_id}"),
        "color": CLUSTER_COLORS.get(c_id, "#6b7280"),
        "state_values": {col: int(row[col]) for col in TOPIC_COLS},
        "cluster_averages": cluster_means,
        "national_averages": national_means,
    }


# ==============================================================================
# FRONTEND DASHBOARD HTML
# ==============================================================================

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSE396 — Regional Search-Interest Clustering Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- FontAwesome CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .tab-btn.active {
            border-bottom: 3px solid #2563eb;
            color: #1e40af;
            font-weight: 600;
        }
        .cluster-badge-0 { background-color: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
        .cluster-badge-1 { background-color: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
        .cluster-badge-2 { background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col">

    <!-- Top Navigation Header -->
    <header class="bg-slate-900 text-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xl shadow">
                    <i class="fa-solid fa-chart-pie"></i>
                </div>
                <div>
                    <h1 class="text-lg font-bold tracking-tight text-white flex items-center gap-2">
                        Regional Search-Interest Pattern Segmentation
                        <span class="text-xs bg-blue-500/30 text-blue-300 px-2 py-0.5 rounded border border-blue-400/30 font-medium">CSE396 Project</span>
                    </h1>
                    <p class="text-xs text-slate-400">Unsupervised K-Means & PCA Analysis across 36 Indian States/UTs • Google Trends</p>
                </div>
            </div>
            <!-- Quick Stat Badges -->
            <div class="flex items-center gap-2 sm:gap-4 text-xs font-medium">
                <span class="bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700">
                    <i class="fa-solid fa-map-pin text-blue-400 mr-1"></i> 36 Regions
                </span>
                <span class="bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700">
                    <i class="fa-solid fa-microchip text-emerald-400 mr-1"></i> 8 Tech Topics
                </span>
                <span class="bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700">
                    <i class="fa-solid fa-cubes text-purple-400 mr-1"></i> Optimal K = 3
                </span>
                <span class="bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700">
                    <i class="fa-solid fa-shield-halved text-amber-400 mr-1"></i> ARI: 0.9500
                </span>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="bg-white border-b border-slate-200">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-1 sm:space-x-8 overflow-x-auto text-sm text-slate-600">
                <button onclick="switchTab('tab-overview')" id="btn-tab-overview" class="tab-btn active py-3 px-3 transition whitespace-nowrap">
                    <i class="fa-solid fa-house mr-1.5"></i> Overview & Problem
                </button>
                <button onclick="switchTab('tab-eda')" id="btn-tab-eda" class="tab-btn py-3 px-3 transition whitespace-nowrap">
                    <i class="fa-solid fa-chart-column mr-1.5"></i> Exploratory Data Analysis
                </button>
                <button onclick="switchTab('tab-validation')" id="btn-tab-validation" class="tab-btn py-3 px-3 transition whitespace-nowrap">
                    <i class="fa-solid fa-diagram-project mr-1.5"></i> K-Means & Validation
                </button>
                <button onclick="switchTab('tab-pca')" id="btn-tab-pca" class="tab-btn py-3 px-3 transition whitespace-nowrap">
                    <i class="fa-solid fa-circle-nodes mr-1.5"></i> 2D PCA Cluster Map
                </button>
                <button onclick="switchTab('tab-profiles')" id="btn-tab-profiles" class="tab-btn py-3 px-3 transition whitespace-nowrap">
                    <i class="fa-solid fa-layer-group mr-1.5"></i> Cluster Profiles & States
                </button>
                <button onclick="switchTab('tab-explorer')" id="btn-tab-explorer" class="tab-btn py-3 px-3 transition whitespace-nowrap">
                    <i class="fa-solid fa-magnifying-glass-location mr-1.5"></i> State Explorer
                </button>
                <button onclick="switchTab('tab-viva')" id="btn-tab-viva" class="tab-btn py-3 px-3 transition whitespace-nowrap">
                    <i class="fa-solid fa-graduation-cap mr-1.5 text-indigo-600"></i> Viva Prep Guide
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">

        <!-- =============================================================== -->
        <!-- TAB 1: OVERVIEW & PROBLEM -->
        <!-- =============================================================== -->
        <section id="tab-overview" class="space-y-6">
            <!-- Ethical Guard Banner -->
            <div class="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-lg shadow-sm">
                <div class="flex items-start">
                    <div class="flex-shrink-0 text-amber-600 mt-0.5 text-lg">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                    </div>
                    <div class="ml-3">
                        <h3 class="text-sm font-semibold text-amber-800">Crucial Ethical Interpretation Principle</h3>
                        <p class="text-xs text-amber-700 mt-1 leading-relaxed">
                            Google Trends search interest represents <strong>relative query volume on Google</strong>, NOT actual intelligence, education level, workforce competence, or adoption rate.
                            Never state: <em>"State X has poor AI knowledge."</em> Always frame accurately: <em>"State X showed relatively lower Google search interest for AI-related terms during the analyzed 12-month period."</em>
                        </p>
                    </div>
                </div>
            </div>

            <!-- Problem & Real-Life Relevance Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <div class="w-9 h-9 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center font-bold mb-3">
                        <i class="fa-solid fa-bullseye"></i>
                    </div>
                    <h2 class="text-lg font-bold text-slate-900 mb-2">The Real-Life Problem</h2>
                    <p class="text-sm text-slate-600 leading-relaxed mb-4">
                        Different geographic regions exhibit vastly different patterns of information demand and curiosity in emerging technologies. However, manually identifying meaningful groups across 36 Indian states and 8 technology domains is impractical and subjective.
                    </p>
                    <p class="text-sm text-slate-600 leading-relaxed">
                        This project formulates an unsupervised machine learning pipeline to automatically discover natural groupings of Indian states that show similar patterns of technology curiosity.
                    </p>
                </div>

                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <div class="w-9 h-9 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold mb-3">
                        <i class="fa-solid fa-hand-holding-heart"></i>
                    </div>
                    <h2 class="text-lg font-bold text-slate-900 mb-2">Practical Applications & Social Value</h2>
                    <ul class="text-sm text-slate-600 space-y-2.5">
                        <li class="flex items-start">
                            <i class="fa-solid fa-check-circle text-emerald-500 mt-1 mr-2 text-xs"></i>
                            <span><strong>Curriculum Planning:</strong> Tailoring university minors & technical electives (e.g. Cloud & Cyber vs. AI & Data Science) to regional demand.</span>
                        </li>
                        <li class="flex items-start">
                            <i class="fa-solid fa-check-circle text-emerald-500 mt-1 mr-2 text-xs"></i>
                            <span><strong>Targeted Skill Development:</strong> Assisting NSDC & state IT councils in directing bootcamps where tech interest is emerging.</span>
                        </li>
                        <li class="flex items-start">
                            <i class="fa-solid fa-check-circle text-emerald-500 mt-1 mr-2 text-xs"></i>
                            <span><strong>Market & Academic Research:</strong> Providing empirical spatial evidence of technology curiosity across India.</span>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Pipeline Workflow Overview -->
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-route text-blue-600"></i> End-to-End Methodology Pipeline
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-center">
                    <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
                        <div class="text-blue-600 font-bold text-xl mb-1">01</div>
                        <div class="text-sm font-semibold text-slate-800">Data Collection</div>
                        <div class="text-xs text-slate-500 mt-1">36 States/UTs x 8 Topics via pytrends (12-month window)</div>
                    </div>
                    <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
                        <div class="text-emerald-600 font-bold text-xl mb-1">02</div>
                        <div class="text-sm font-semibold text-slate-800">Preprocessing</div>
                        <div class="text-xs text-slate-500 mt-1">Audit zeros, separate identifiers, StandardScaler (mean=0, std=1)</div>
                    </div>
                    <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
                        <div class="text-purple-600 font-bold text-xl mb-1">03</div>
                        <div class="text-sm font-semibold text-slate-800">K-Means & Validation</div>
                        <div class="text-xs text-slate-500 mt-1">WCSS, Silhouette, Davies-Bouldin, K-Medoids (L1) comparison</div>
                    </div>
                    <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
                        <div class="text-amber-600 font-bold text-xl mb-1">04</div>
                        <div class="text-sm font-semibold text-slate-800">PCA & Profiling</div>
                        <div class="text-xs text-slate-500 mt-1">2D PCA (89.33% variance), stability analysis (ARI=0.95)</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- TAB 2: EXPLORATORY DATA ANALYSIS -->
        <!-- =============================================================== -->
        <section id="tab-eda" class="space-y-6 hidden">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Topic Distributions Card -->
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-2 flex items-center gap-2">
                        <i class="fa-solid fa-chart-simple text-blue-600"></i> Topic Search-Interest Distributions
                    </h3>
                    <p class="text-xs text-slate-500 mb-4">Spread and range of 0–100 search intensity across all 36 Indian states.</p>
                    <img src="/figures/topic_distributions.png" alt="Topic Distributions" class="w-full rounded-lg border border-slate-100 shadow-sm">
                </div>

                <!-- Top States Ranking Card -->
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-2 flex items-center gap-2">
                        <i class="fa-solid fa-ranking-star text-amber-500"></i> Top 15 States by Mean Tech Curiosity
                    </h3>
                    <p class="text-xs text-slate-500 mb-4">Overall average search interest across all 8 emerging technology domains.</p>
                    <img src="/figures/state_tech_interest_comparison.png" alt="State Comparison" class="w-full rounded-lg border border-slate-100 shadow-sm">
                </div>
            </div>

            <!-- Inter-Topic Correlation Card -->
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex flex-col lg:flex-row gap-6 items-center">
                    <div class="w-full lg:w-1/2">
                        <h3 class="text-base font-bold text-slate-900 mb-2 flex items-center gap-2">
                            <i class="fa-solid fa-fire-flame-curved text-red-500"></i> Inter-Topic Pearson Correlation Heatmap
                        </h3>
                        <p class="text-xs text-slate-600 mb-3 leading-relaxed">
                            <strong>Key Correlation Findings:</strong>
                        </p>
                        <ul class="text-xs text-slate-600 space-y-2">
                            <li class="flex items-start">
                                <span class="text-blue-600 font-bold mr-2">•</span>
                                <span><strong>High Core Association:</strong> AI and Machine Learning (r = 0.88), Data Science (r = 0.84), and Cybersecurity (r = 0.87) strongly co-occur.</span>
                            </li>
                            <li class="flex items-start">
                                <span class="text-blue-600 font-bold mr-2">•</span>
                                <span><strong>Consumer AI Divergence:</strong> ChatGPT exhibits moderate correlation (r ≈ 0.54–0.74) across all regions, reflecting broad public curiosity.</span>
                            </li>
                            <li class="flex items-start">
                                <span class="text-blue-600 font-bold mr-2">•</span>
                                <span><strong>IoT Independence:</strong> Internet of Things has low correlation with ChatGPT (r = 0.26), representing unique hardware/embedded demand.</span>
                            </li>
                        </ul>
                    </div>
                    <div class="w-full lg:w-1/2">
                        <img src="/figures/topic_correlation_heatmap.png" alt="Correlation Heatmap" class="w-full rounded-lg border border-slate-100 shadow-sm max-h-[380px] object-contain">
                    </div>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- TAB 3: K-MEANS EXPERIMENTS & VALIDATION -->
        <!-- =============================================================== -->
        <section id="tab-validation" class="space-y-6 hidden">
            <!-- Multi-Metric Validation Table -->
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex flex-wrap justify-between items-center mb-4 gap-2">
                    <div>
                        <h3 class="text-base font-bold text-slate-900">K-Means Multi-Metric Validation Table</h3>
                        <p class="text-xs text-slate-500">Evaluation across candidate cluster counts with fixed random_state = 42.</p>
                    </div>
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-semibold px-2.5 py-1 rounded-full border border-emerald-300">
                        Selected: K = 3 (Elbow Point & Actionable Tiers)
                    </span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm border-collapse">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 text-xs uppercase tracking-wider">
                                <th class="p-3 font-semibold">Cluster Count (K)</th>
                                <th class="p-3 font-semibold">WCSS / Inertia (Lower = Tighter)</th>
                                <th class="p-3 font-semibold">Silhouette Score (Higher = Better)</th>
                                <th class="p-3 font-semibold">Davies-Bouldin Index (Lower = Better)</th>
                                <th class="p-3 font-semibold">Evaluation & Decision</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200 text-slate-700 text-sm">
                            <tr class="hover:bg-slate-50">
                                <td class="p-3 font-bold">K = 2</td>
                                <td class="p-3 font-mono">116.37</td>
                                <td class="p-3 font-mono text-emerald-600 font-semibold">0.5150</td>
                                <td class="p-3 font-mono text-emerald-600 font-semibold">0.7134</td>
                                <td class="p-3 text-xs text-slate-500">Highest statistical separation; coarse binary split (too coarse for policy).</td>
                            </tr>
                            <tr class="bg-blue-50/60 font-semibold border-l-4 border-blue-600">
                                <td class="p-3 font-bold text-blue-900">K = 3 (Selected)</td>
                                <td class="p-3 font-mono text-blue-900">88.39 (-24.0%)</td>
                                <td class="p-3 font-mono text-blue-900">0.3011</td>
                                <td class="p-3 font-mono text-blue-900">1.0499</td>
                                <td class="p-3 text-xs text-blue-900 font-medium">Defensible Elbow inflection; 3 actionable tiers (Hubs, Moderate, Emerging).</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3 font-bold">K = 4</td>
                                <td class="p-3 font-mono">66.49</td>
                                <td class="p-3 font-mono">0.3483</td>
                                <td class="p-3 font-mono">0.9886</td>
                                <td class="p-3 text-xs text-slate-500">Isolates smaller 2–3 state sub-groups; diminishing return.</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3 font-bold">K = 5</td>
                                <td class="p-3 font-mono">55.48</td>
                                <td class="p-3 font-mono">0.3556</td>
                                <td class="p-3 font-mono">0.9000</td>
                                <td class="p-3 text-xs text-slate-500">Over-fragments the 36 observations into small groups.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Elbow Curve & Metrics Plots -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-2">Elbow Method & Validation Curves</h3>
                    <p class="text-xs text-slate-500 mb-4">WCSS, Silhouette, and Davies-Bouldin progression across K=2, 3, 4, 5.</p>
                    <img src="/figures/elbow_and_validation_metrics.png" alt="Validation Curves" class="w-full rounded-lg border border-slate-100 shadow-sm">
                </div>

                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-2">Distance Geometry: Euclidean vs Manhattan</h3>
                    <p class="text-xs text-slate-500 mb-4">Comparison of Euclidean K-Means (L2) vs Manhattan K-Medoids (L1).</p>
                    <img src="/figures/distance_metric_comparison.png" alt="Distance Comparison" class="w-full rounded-lg border border-slate-100 shadow-sm">
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- TAB 4: 2D PCA CLUSTER MAP -->
        <!-- =============================================================== -->
        <section id="tab-pca" class="space-y-6 hidden">
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex flex-wrap justify-between items-center mb-4 gap-2">
                    <div>
                        <h3 class="text-base font-bold text-slate-900">Interactive 2D PCA Cluster Map (K = 3)</h3>
                        <p class="text-xs text-slate-500">
                            Principal Component Analysis reduces 8 dimensions to 2 components while retaining <strong>89.33% of total variance</strong> (PC1: 79.27%, PC2: 10.06%).
                        </p>
                    </div>
                    <div class="flex items-center gap-3 text-xs">
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-blue-600 inline-block"></span> Cluster 0 (Hubs)</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span> Cluster 1 (Moderate)</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-amber-500 inline-block"></span> Cluster 2 (Emerging)</span>
                    </div>
                </div>

                <!-- High-Resolution Rendered PCA Plot -->
                <div class="mb-6">
                    <img src="/figures/pca_cluster_visualization.png" alt="PCA Cluster Visualization" class="w-full rounded-lg border border-slate-100 shadow-sm max-h-[520px] object-contain mx-auto">
                </div>

                <!-- Interactive Canvas for State Hover Tooltip -->
                <div class="border-t border-slate-100 pt-4">
                    <h4 class="text-sm font-semibold text-slate-800 mb-2">Explore 2D Projection Coordinates & Values:</h4>
                    <div class="h-80 w-full">
                        <canvas id="pcaChart"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- TAB 5: CLUSTER PROFILES & REGIONS -->
        <!-- =============================================================== -->
        <section id="tab-profiles" class="space-y-6 hidden">
            <!-- Cluster Profiles Heatmap & Bar Chart -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-2">Standardized Z-Score Cluster Profile Heatmap</h3>
                    <p class="text-xs text-slate-500 mb-4">Shows how many standard deviations each cluster deviates from national averages.</p>
                    <img src="/figures/cluster_profile_heatmap.png" alt="Profile Heatmap" class="w-full rounded-lg border border-slate-100 shadow-sm">
                </div>

                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-2">Topic Search Index (0–100) Comparison</h3>
                    <p class="text-xs text-slate-500 mb-4">Raw Google Trends search intensity averages across the 3 clusters.</p>
                    <img src="/figures/cluster_topic_comparison.png" alt="Topic Comparison Bar Chart" class="w-full rounded-lg border border-slate-100 shadow-sm">
                </div>
            </div>

            <!-- Complete State-to-Cluster Mapping Table -->
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex flex-wrap justify-between items-center mb-4 gap-2">
                    <div>
                        <h3 class="text-base font-bold text-slate-900">All 36 Indian States & UTs by Discovered Cluster</h3>
                        <p class="text-xs text-slate-500">Filter or search any state to view its cluster affiliation and search scores.</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <input type="text" id="stateSearchInput" onkeyup="filterStateTable()" placeholder="Search state name..." class="text-xs px-3 py-1.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <select id="clusterFilterSelect" onchange="filterStateTable()" class="text-xs px-3 py-1.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="all">All Clusters</option>
                            <option value="0">Cluster 0 (Hubs)</option>
                            <option value="1">Cluster 1 (Moderate)</option>
                            <option value="2">Cluster 2 (Emerging)</option>
                        </select>
                    </div>
                </div>

                <div class="overflow-x-auto max-h-96">
                    <table class="w-full text-left text-xs border-collapse" id="allStatesTable">
                        <thead class="sticky top-0 bg-slate-100 text-slate-700 font-semibold uppercase">
                            <tr>
                                <th class="p-2.5">State / UT</th>
                                <th class="p-2.5">Cluster</th>
                                <th class="p-2.5">AI</th>
                                <th class="p-2.5">ML</th>
                                <th class="p-2.5">Data Sci</th>
                                <th class="p-2.5">Cloud</th>
                                <th class="p-2.5">Cyber</th>
                                <th class="p-2.5">Blockch</th>
                                <th class="p-2.5">IoT</th>
                                <th class="p-2.5">ChatGPT</th>
                                <th class="p-2.5 font-bold">Mean</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200 text-slate-700" id="statesTableBody">
                            <!-- Populated dynamically via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- TAB 6: INTERACTIVE STATE EXPLORER -->
        <!-- =============================================================== -->
        <section id="tab-explorer" class="space-y-6 hidden">
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div class="max-w-xl mx-auto text-center mb-6">
                    <h3 class="text-lg font-bold text-slate-900 mb-1">Interactive Regional Profile Inspector</h3>
                    <p class="text-xs text-slate-500">Select any Indian State or Union Territory to inspect its 8-topic radar fingerprint compared to its cluster average and the national benchmark.</p>
                    <div class="mt-4">
                        <select id="stateSelectDropdown" onchange="loadStateRadar()" class="w-full max-w-md mx-auto text-sm px-4 py-2 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium text-slate-800">
                            <!-- Populated dynamically via JS -->
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
                    <!-- Left: Metadata & Rank Card -->
                    <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-4 text-sm" id="stateMetadataCard">
                        <h4 class="font-bold text-slate-900 text-base" id="cardStateName">Loading...</h4>
                        <div>
                            <span class="text-xs text-slate-500 uppercase font-semibold">Assigned Cluster</span>
                            <div class="mt-1" id="cardClusterBadge"></div>
                        </div>
                        <div>
                            <span class="text-xs text-slate-500 uppercase font-semibold">Mean Search Intensity (0–100)</span>
                            <div class="text-2xl font-extrabold text-slate-900 mt-1" id="cardMeanScore">--</div>
                        </div>
                        <div class="pt-2 border-t border-slate-200 text-xs text-slate-600 space-y-1.5" id="cardTopicBreakdown">
                            <!-- Populated dynamically -->
                        </div>
                    </div>

                    <!-- Right: Radar Chart (2 cols) -->
                    <div class="lg:col-span-2 bg-white p-4 rounded-xl border border-slate-100 flex items-center justify-center">
                        <div class="w-full max-w-md h-80">
                            <canvas id="stateRadarChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- TAB 7: VIVA PREPARATION GUIDE -->
        <!-- =============================================================== -->
        <section id="tab-viva" class="space-y-6 hidden">
            <div class="bg-indigo-50 border border-indigo-200 rounded-xl p-6 shadow-sm">
                <div class="flex items-center gap-3 mb-2">
                    <div class="w-10 h-10 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-lg">
                        <i class="fa-solid fa-graduation-cap"></i>
                    </div>
                    <div>
                        <h2 class="text-lg font-bold text-indigo-950">CSE396 Viva Voce Comprehensive Q&A Hub</h2>
                        <p class="text-xs text-indigo-700">All 26 Viva Questions and Student-Friendly Explanations</p>
                    </div>
                </div>
            </div>

            <!-- Accordion List -->
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm divide-y divide-slate-200 text-sm" id="vivaAccordionList">
                <!-- Populated dynamically with all 26 Q&As -->
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-slate-900 text-slate-400 py-6 border-t border-slate-800 text-center text-xs">
        <p>CSE396 Unsupervised Learning Project • B.Tech CSE • Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering</p>
        <p class="mt-1 text-slate-500">Google Trends open data • K-Means • K-Medoids • PCA • StandardScaler</p>
    </footer>

    <!-- Frontend Interactive Script -->
    <script>
        let allStatesData = [];
        let pcaChartInstance = null;
        let radarChartInstance = null;

        // Switch Navigation Tabs
        function switchTab(tabId) {
            document.querySelectorAll('main > section').forEach(sec => sec.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabId).classList.remove('hidden');
            document.getElementById('btn-' + tabId).classList.add('active');

            if (tabId === 'tab-pca' && !pcaChartInstance) {
                initPcaChart();
            }
        }

        // Initialize App Data
        async function initDashboard() {
            try {
                const resStates = await fetch('/api/states');
                allStatesData = await resStates.json();
                renderStatesTable(allStatesData);
                populateStateDropdown(allStatesData);
                loadStateRadar();
                renderVivaAccordion();
            } catch (err) {
                console.error("Dashboard Init Error:", err);
            }
        }

        // Render All States Table
        function renderStatesTable(data) {
            const tbody = document.getElementById('statesTableBody');
            tbody.innerHTML = '';
            data.forEach(item => {
                const badgeClass = item.cluster === 0 ? 'cluster-badge-0' : (item.cluster === 1 ? 'cluster-badge-1' : 'cluster-badge-2');
                const row = document.createElement('tr');
                row.className = "hover:bg-slate-50";
                row.innerHTML = `
                    <td class="p-2.5 font-semibold text-slate-900">${item.state} <span class="text-slate-400 text-[10px]">(${item.geo_code})</span></td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[11px] font-semibold ${badgeClass}">Cluster ${item.cluster}</span></td>
                    <td class="p-2.5 font-mono">${item.topics.artificial_intelligence}</td>
                    <td class="p-2.5 font-mono">${item.topics.machine_learning}</td>
                    <td class="p-2.5 font-mono">${item.topics.data_science}</td>
                    <td class="p-2.5 font-mono">${item.topics.cloud_computing}</td>
                    <td class="p-2.5 font-mono">${item.topics.cybersecurity}</td>
                    <td class="p-2.5 font-mono">${item.topics.blockchain}</td>
                    <td class="p-2.5 font-mono">${item.topics.internet_of_things}</td>
                    <td class="p-2.5 font-mono">${item.topics.chatgpt}</td>
                    <td class="p-2.5 font-mono font-bold text-blue-700">${item.mean_index}</td>
                `;
                tbody.appendChild(row);
            });
        }

        // Filter State Table
        function filterStateTable() {
            const searchVal = document.getElementById('stateSearchInput').value.toLowerCase();
            const clusterVal = document.getElementById('clusterFilterSelect').value;

            const filtered = allStatesData.filter(item => {
                const matchName = item.state.toLowerCase().includes(searchVal);
                const matchCluster = (clusterVal === 'all') || (item.cluster.toString() === clusterVal);
                return matchName && matchCluster;
            });
            renderStatesTable(filtered);
        }

        // Populate State Dropdown
        function populateStateDropdown(data) {
            const select = document.getElementById('stateSelectDropdown');
            select.innerHTML = '';
            data.forEach(item => {
                const opt = document.createElement('option');
                opt.value = item.state;
                opt.textContent = `${item.state} (Cluster ${item.cluster})`;
                select.appendChild(opt);
            });
            select.value = "Karnataka"; // Default
        }

        // Load State Radar
        async function loadStateRadar() {
            const stateName = document.getElementById('stateSelectDropdown').value || "Karnataka";
            try {
                const res = await fetch(`/api/state/${encodeURIComponent(stateName)}`);
                const data = await res.json();

                // Update card
                document.getElementById('cardStateName').textContent = `${data.state} (${data.geo_code})`;
                const badgeClass = data.cluster === 0 ? 'cluster-badge-0' : (data.cluster === 1 ? 'cluster-badge-1' : 'cluster-badge-2');
                document.getElementById('cardClusterBadge').innerHTML = `<span class="px-2.5 py-1 rounded-md text-xs font-semibold ${badgeClass}">Cluster ${data.cluster}: ${data.cluster_name}</span>`;
                
                const scores = Object.values(data.state_values);
                const meanScore = (scores.reduce((a, b) => a + b, 0) / scores.length).round ? (scores.reduce((a, b) => a + b, 0) / scores.length).round(1) : (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);
                document.getElementById('cardMeanScore').textContent = `${meanScore} / 100`;

                // Breakdown
                const topicLabels = ["Artificial Intelligence", "Machine Learning", "Data Science", "Cloud Computing", "Cybersecurity", "Blockchain", "Internet of Things", "ChatGPT"];
                const topicKeys = ["artificial_intelligence", "machine_learning", "data_science", "cloud_computing", "cybersecurity", "blockchain", "internet_of_things", "chatgpt"];

                let bHtml = '<div class="grid grid-cols-2 gap-2 mt-2">';
                topicKeys.forEach((key, idx) => {
                    bHtml += `<div class="flex justify-between border-b border-slate-200 pb-1">
                        <span class="text-slate-500">${topicLabels[idx].substring(0, 12)}...</span>
                        <span class="font-bold text-slate-800 font-mono">${data.state_values[key]}</span>
                    </div>`;
                });
                bHtml += '</div>';
                document.getElementById('cardTopicBreakdown').innerHTML = bHtml;

                // Render Radar Chart
                const ctx = document.getElementById('stateRadarChart').getContext('2d');
                if (radarChartInstance) radarChartInstance.destroy();

                radarChartInstance = new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: topicLabels,
                        datasets: [
                            {
                                label: data.state,
                                data: topicKeys.map(k => data.state_values[k]),
                                backgroundColor: 'rgba(37, 99, 235, 0.25)',
                                borderColor: '#2563eb',
                                borderWidth: 2,
                                pointBackgroundColor: '#2563eb'
                            },
                            {
                                label: `Cluster ${data.cluster} Average`,
                                data: topicKeys.map(k => data.cluster_averages[k]),
                                backgroundColor: 'rgba(16, 185, 129, 0.15)',
                                borderColor: '#10b981',
                                borderWidth: 1.5,
                                borderDash: [4, 4],
                                pointBackgroundColor: '#10b981'
                            },
                            {
                                label: 'National Average',
                                data: topicKeys.map(k => data.national_averages[k]),
                                backgroundColor: 'rgba(156, 163, 175, 0.1)',
                                borderColor: '#9ca3af',
                                borderWidth: 1,
                                borderDash: [2, 2],
                                pointBackgroundColor: '#9ca3af'
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            r: {
                                min: 0,
                                max: 100,
                                ticks: { stepSize: 25, font: { size: 9 } },
                                pointLabels: { font: { size: 10, weight: 'bold' } }
                            }
                        },
                        plugins: {
                            legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } }
                        }
                    }
                });

            } catch (err) {
                console.error("State Radar Error:", err);
            }
        }

        // Initialize 2D PCA Chart
        async function initPcaChart() {
            try {
                const res = await fetch('/api/pca_data');
                const data = await res.json();
                const ctx = document.getElementById('pcaChart').getContext('2d');

                const clusterGroups = { 0: [], 1: [], 2: [] };
                data.forEach(item => {
                    clusterGroups[item.cluster].push({
                        x: item.pc1,
                        y: item.pc2,
                        state: item.state,
                        cluster_name: item.cluster_name
                    });
                });

                pcaChartInstance = new Chart(ctx, {
                    type: 'scatter',
                    data: {
                        datasets: [
                            {
                                label: 'Cluster 0: Tech Hubs',
                                data: clusterGroups[0],
                                backgroundColor: '#2563eb',
                                pointRadius: 6,
                                pointHoverRadius: 9
                            },
                            {
                                label: 'Cluster 1: Moderate Demand',
                                data: clusterGroups[1],
                                backgroundColor: '#10b981',
                                pointRadius: 6,
                                pointHoverRadius: 9
                            },
                            {
                                label: 'Cluster 2: Emerging Demand',
                                data: clusterGroups[2],
                                backgroundColor: '#f59e0b',
                                pointRadius: 6,
                                pointHoverRadius: 9
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: { title: { display: true, text: 'Principal Component 1 (79.27% Variance)', font: { weight: 'bold' } } },
                            y: { title: { display: true, text: 'Principal Component 2 (10.06% Variance)', font: { weight: 'bold' } } }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        const p = ctx.raw;
                                        return `${p.state} (${p.cluster_name}): [PC1: ${p.x}, PC2: ${p.y}]`;
                                    }
                                }
                            },
                            legend: { position: 'bottom' }
                        }
                    }
                });
            } catch (err) {
                console.error("PCA Chart Init Error:", err);
            }
        }

        // 26 Viva Questions Data
        const vivaData = [
            { q: "1. What problem does this project solve?", a: "It solves the difficulty of manually identifying meaningful patterns of curiosity and demand for emerging technologies across 36 Indian states and union territories. It uses unsupervised clustering to group states with similar search demand automatically." },
            { q: "2. How is it connected to a real-life problem?", a: "Education planners (e.g., universities) and policy bodies (e.g., NSDC) need empirical evidence to direct curriculum minors, bootcamps, and awareness workshops where demand is emerging." },
            { q: "3. What is Google Trends?", a: "A public analytics platform by Google that indexes the relative search query popularity across geographic regions and timeframes." },
            { q: "4. What does Google Trends search interest mean?", a: "It is a normalized index (0–100) representing search volume relative to the peak region in the query context. It measures curiosity, never total population or competence." },
            { q: "5. What is unsupervised learning?", a: "A branch of machine learning where models discover intrinsic patterns or groupings from unlabeled data without pre-existing target labels." },
            { q: "6. Why is this an unsupervised learning problem?", a: "There are no pre-existing ground-truth labels telling us which state belongs to which cluster. The model discovers groups based on similarity." },
            { q: "7. What is clustering?", a: "Partitioning unlabeled data into groups such that points within the same cluster have high cohesion and points in different clusters have high separation." },
            { q: "8. Why did we use K-Means?", a: "It is computationally efficient, mathematically sound for continuous features, and provides clear interpretable centroids." },
            { q: "9. What is K?", a: "The user-defined hyperparameter indicating the number of clusters to partition the data into." },
            { q: "10. What is a centroid?", a: "The arithmetic mean position of all data points belonging to a specific cluster in multidimensional space." },
            { q: "11. Why is feature scaling required?", a: "Distance-based algorithms like K-Means are sensitive to variance differences. Scaling prevents high-variance topics from dominating Euclidean distance." },
            { q: "12. What is StandardScaler?", a: "A transformation that standardizes features by subtracting the mean and dividing by standard deviation (z = (x - mean) / std), giving mean=0 and std=1." },
            { q: "13. What is Euclidean distance?", a: "The straight-line geometric distance (L2 norm) between two points in multidimensional space: d = sqrt(sum((x_i - y_i)^2))." },
            { q: "14. What is Manhattan distance?", a: "The sum of absolute coordinate differences (L1 norm or taxicab distance): d = sum(|x_i - y_i|)." },
            { q: "15. Why doesn't standard K-Means directly use Manhattan distance?", a: "The arithmetic mean centroid minimizes squared Euclidean distance (L2). Minimizing Manhattan distance (L1) requires the median. Using Manhattan distance with the mean is mathematically inconsistent; K-Medoids (PAM) is used instead." },
            { q: "16. What is WCSS / Inertia?", a: "Within-Cluster Sum of Squares measures cluster compactness by summing squared Euclidean distances from every point to its assigned centroid." },
            { q: "17. What is the Elbow Method?", a: "A heuristic that plots WCSS against K to find the inflection point ('elbow') where the rate of variance reduction diminishes sharply." },
            { q: "18. What is the Silhouette Score?", a: "A metric measuring cohesion vs. separation ranging from -1 to +1. Values closer to +1 indicate well-separated, cohesive clusters." },
            { q: "19. What is the Davies-Bouldin Index?", a: "A metric measuring average similarity between each cluster and its most similar one. Lower values indicate tighter, better-separated clusters." },
            { q: "20. What is PCA?", a: "Principal Component Analysis is an unsupervised linear technique that transforms correlated dimensions into orthogonal principal components of maximum variance." },
            { q: "21. Why was PCA used in this project?", a: "To reduce the 8-dimensional standardized space into 2 dimensions for visualization, retaining 89.33% of total multidimensional variance." },
            { q: "22. How was optimal K selected?", a: "K=3 was selected by combining the Elbow Method (24.0% drop in WCSS), solid silhouette score (0.3011), and actionable real-world policy utility (Hubs, Moderate, Emerging)." },
            { q: "23. What do the discovered clusters represent?", a: "Cluster 0: High-Intensity Tech Hubs (Telangana, Karnataka, Delhi, Maharashtra); Cluster 1: Moderate Demand States (Gujarat, Kerala, UP); Cluster 2: Emerging Demand Regions (North-East, Bihar)." },
            { q: "24. How stable are these clusters?", a: "Tested across 10 random seeds using Adjusted Rand Index (ARI), achieving a mean ARI of 0.9500, indicating exceptional cluster stability." },
            { q: "25. What are the key limitations?", a: "Search interest does not equal technical ability; language bias (English/Hindi focus); Google Trends sampling variations; PCA information loss (10.67%)." },
            { q: "26. What are the ethical concerns?", a: "Clusters represent search patterns, never the people. Do not stereotype states or use clusters for discriminatory hiring or automated high-stakes decisions." }
        ];

        // Render Viva Accordion
        function renderVivaAccordion() {
            const container = document.getElementById('vivaAccordionList');
            container.innerHTML = '';
            vivaData.forEach((item, idx) => {
                const itemDiv = document.createElement('div');
                itemDiv.className = "p-4 hover:bg-slate-50 transition";
                itemDiv.innerHTML = `
                    <button onclick="toggleViva(${idx})" class="w-full text-left font-semibold text-slate-900 flex justify-between items-center focus:outline-none">
                        <span>${item.q}</span>
                        <i id="viva-icon-${idx}" class="fa-solid fa-chevron-down text-xs text-slate-400 transition-transform"></i>
                    </button>
                    <div id="viva-ans-${idx}" class="hidden mt-2.5 text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
                        ${item.a}
                    </div>
                `;
                container.appendChild(itemDiv);
            });
        }

        function toggleViva(idx) {
            const ans = document.getElementById(`viva-ans-${idx}`);
            const icon = document.getElementById(`viva-icon-${idx}`);
            if (ans.classList.contains('hidden')) {
                ans.classList.remove('hidden');
                icon.style.transform = 'rotate(180deg)';
            } else {
                ans.classList.add('hidden');
                icon.style.transform = 'rotate(0deg)';
            }
        }

        // Start
        window.onload = initDashboard;
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serve the complete interactive web dashboard."""
    return HTMLResponse(content=HTML_CONTENT)


def launch():
    """Run Uvicorn server and open browser automatically."""
    port = 8000
    host = "127.0.0.1"
    url = f"http://{host}:{port}"

    print("=" * 70)
    print("CSE396 - Interactive Web Application Starting")
    print("=" * 70)
    print(f"[LAUNCH] Dashboard running at: {url}")
    print("[INFO] Opening interactive web application in your default browser...")
    print("[INFO] Press Ctrl+C in terminal to stop server.\n")

    # Open browser automatically after 1.5 seconds
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()

    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    launch()

