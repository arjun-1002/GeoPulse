# Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering

**Course:** CSE396 — Unsupervised Learning  
**Official Project Title:** *Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering*  
**Application Domain:** Tourism Planning & Analytics  
**Application Name:** **Regional Tourism Promotion Planner**  
**Subtitle:** *An AI-Powered Tourism Planning Support System for Indian States and Union Territories*  
**Author:** Arjun (B.Tech in Computer Science & Engineering)  

---

## 🌟 Executive Overview

This repository contains the complete, production-grade university project for **CSE396 Unsupervised Learning**. 

The system analyzes Google Trends search-interest patterns across Indian States and Union Territories across multiple key domains (such as Tourism topics: *Tourism, Travel, Beaches, Hill stations, Wildlife tourism, Religious tourism*, as well as emerging technology domains). It applies unsupervised machine learning algorithms (**K-Means** with Euclidean $L_2$ distance and **K-Medians** with Manhattan $L_1$ distance) to uncover regional demand patterns, evaluate clustering quality, visualize segments via 2D/3D PCA, and generate empirical decision-support planning recommendations for regional development.

The project features a **modern, interactive multi-page web application built with Streamlit and Plotly**, alongside modular Python pipelines and an executed Jupyter Notebook.

---

## 🚀 Quick Start — How to Run the Web Application

### 1. Environment Setup
```bash
# Navigate to the project directory
cd "cse396 new"

# Install required dependencies
pip install -r requirements.txt
```

### 2. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
*(Your default web browser will automatically open `http://localhost:8501` to display the dashboard).*

### 3. Demonstration Mode vs Real Data
- **Demonstration Mode (Default / 1-Click):** If you don't have raw Google Trends CSVs on hand, click **"Load Synthetic Demonstration Dataset"** on the Home page or Data Upload page. This loads a realistic 24-state $\times$ 6-topic $\times$ 157-week synthetic benchmark so you can immediately explore the entire clustering pipeline, interactive 2D/3D PCA charts, radar fingerprints, and planning recommendations.
- **Real Google Trends Data:** Download weekly CSV files from Google Trends for Indian States/UTs (Web Search, Nov 2023 – Nov 2026), upload them on page **2. Data Upload**, run preprocessing and feature engineering, and cluster real observations!

---

## 🧭 Multi-Page Web Application Structure

The application features 9 structured modules in the navigation sidebar:

1. **🏠 1. Home Dashboard (`pages/1_Home.py`)**  
   Executive overview card, project identity, status summary metrics, active dataset indicator, decision safeguards, and demonstration data loader.

2. **📥 2. Data Upload (`pages/2_Data_Upload.py`)**  
   Drag-and-drop uploader for Google Trends CSVs, automated topic and region inference, metadata editor, dataset preview, and demonstration mode switch.

3. **🧹 3. Data Quality & Preprocessing (`pages/3_Preprocessing.py`)**  
   Data quality audit, weekly Sunday calendar alignment (`W-SUN`), short-gap interpolation ($\le 2$ weeks), zero-value preservation, and internal series standardization ($Z$-score).

4. **⚙️ 4. Feature Engineering (`pages/4_Feature_Engineering.py`)**  
   Regional aggregation (one row per State/UT), 7 features per topic (42 total: Quarterly $Q_1-Q_4$ averages, Annual baseline, Volatility, and OLS Trend Slope), median imputation, and `StandardScaler`.

5. **🔬 5. Clustering Analysis (`pages/5_Clustering.py`)**  
   Dual clustering algorithm selection:
   - **K-Means** (Euclidean $L_2$ distance, $n\_init=50$, Lloyd's algorithm)
   - **K-Medians** (Manhattan $L_1$ distance with coordinate-wise median updates)  
   Interactive $K \in [2, 5]$ slider, Elbow plot, Silhouette score, Davies-Bouldin index, and multi-seed stability (ARI across 10 random initializations).

6. **📊 6. PCA Visualization (`pages/6_PCA_Visualization.py`)**  
   Interactive 2D & 3D PCA scatter plots with Plotly, state hover cards, explained variance percentages, and principal component loadings.

7. **💡 7. Cluster Insights (`pages/7_Cluster_Insights.py`)**  
   Regional membership directories, cluster size distributions, seasonal radar profiles, and centroid tables.

8. **🎯 8. Tourism Planning Recommendations (`pages/8_Planning_Recommendations.py`)**  
   Evidence-based promotional campaign hypotheses, seasonal launch windows, strategic rationales, field validation metrics, CSV exports, and executive HTML report generator.

9. **📖 9. About the Project (`pages/9_About.py`)**  
   Academic documentation, research problem statement, 8 methodology objectives, K-Means vs K-Medians comparison table, and ethical interpretation guidelines.

---

## 🔬 Clustering Algorithms & Mathematical Foundations

### K-Means vs K-Medians Comparison
| Dimension | K-Means Clustering | K-Medians Clustering |
| :--- | :--- | :--- |
| **Distance Metric** | Squared Euclidean Distance ($L_2$ norm) | Manhattan Distance ($L_1$ norm) |
| **Objective Function** | $\min \sum_{k} \sum_{x \in C_k} \|x - \mu_k\|_2^2$ | $\min \sum_{k} \sum_{x \in C_k} \|x - m_k\|_1$ |
| **Centroid Computation**| Arithmetic mean $\mu_k = \frac{1}{|C_k|} \sum x$ | Coordinate-wise median $m_k = \text{median}(x)$ |
| **Outlier Sensitivity**| Sensitive to extreme search spikes | Robust against viral search spikes and skewed outliers |
| **Optimization** | Lloyd's algorithm (`scikit-learn`) | Custom iterative Expectation-Maximization |

### Feature Engineering Details
For each region $r$ and topic $j$, weekly standardized time series $z_{r, j, t}$ are transformed into 7 features:
- **$Q_1$ Seasonal Mean:** $\frac{1}{N_{Q1}} \sum_{t \in Q1} z_t$ (January – March)
- **$Q_2$ Seasonal Mean:** $\frac{1}{N_{Q2}} \sum_{t \in Q2} z_t$ (April – June)
- **$Q_3$ Seasonal Mean:** $\frac{1}{N_{Q3}} \sum_{t \in Q3} z_t$ (July – September)
- **$Q_4$ Seasonal Mean:** $\frac{1}{N_{Q4}} \sum_{t \in Q4} z_t$ (October – December)
- **Annual Mean:** Baseline search engagement level across all weeks.
- **Seasonal Volatility:** Standard deviation $\sigma$, reflecting cyclical demand swings.
- **Trend Slope ($\beta_1$):** OLS regression slope indicating multi-year interest trajectory.

---

## 🛡️ Critical Interpretation Safeguards & Limitations

1. **Search Interest $\neq$ Footfall or Competence:**  
   Google Trends measures relative search query interest on Google Web Search. It does **not** measure physical tourist arrivals, economic spending, or resident capabilities.
2. **Digital Divide & Normalization:**  
   Google Trends values are normalized by total regional search queries. Regions with lower internet penetration are evaluated relative to their own search base, not total population.
3. **Synthetic Demonstration Notice:**  
   When running in Demonstration Mode, all outputs are marked clearly as synthetic test data and must never be cited as real empirical findings.
4. **Mandatory Field Validation:**  
   Prior to budget allocations, government agencies must cross-reference suggestions with official Ministry of Tourism statistics, hotel occupancy surveys, and transit data.

---

## 📂 Project Architecture

```
cse396 new/
├── app.py                            # Root Streamlit Application Entrypoint
├── pages/
│   ├── 1_Home.py                     # Home Executive Dashboard
│   ├── 2_Data_Upload.py              # Google Trends CSV Ingestion & Demo Loader
│   ├── 3_Preprocessing.py            # Quality Audit & Preprocessing Pipeline
│   ├── 4_Feature_Engineering.py      # Regional Feature Matrix Construction
│   ├── 5_Clustering.py               # K-Means & K-Medians Clustering Engine
│   ├── 6_PCA_Visualization.py        # 2D & 3D Interactive Dimensionality Reduction
│   ├── 7_Cluster_Insights.py         # Membership Directories & Radar Profiles
│   ├── 8_Planning_Recommendations.py # Evidence-Based Strategic Planning
│   └── 9_About.py                    # Academic Documentation & Methodology
├── modules/
│   ├── data_loader.py                # Google Trends Parser & Synthetic Demo Generator
│   ├── data_validation.py            # Quality Audit & Bound Checks
│   ├── preprocessing.py              # Calendar Alignment & Standardization
│   ├── feature_engineering.py        # 42 Seasonal Regional Indicators
│   ├── clustering.py                 # K-Means & Custom Manhattan K-Medians
│   ├── visualization.py              # Plotly Visualizations (PCA, Elbow, Radar)
│   ├── recommendations.py            # Promotional Hypotheses Generator
│   ├── report_generator.py           # HTML Executive Report Builder
│   └── state_manager.py              # Session State & Theme Management
├── notebooks/
│   └── regional_search_clustering.ipynb # Executed Jupyter Notebook
├── src/                              # Standalone CLI Scripts (Days 1–4)
│   ├── data_collection.py
│   ├── preprocessing.py
│   ├── clustering.py
│   └── visualization.py
├── outputs/                          # Generated Figures, CSVs & Tables
├── requirements.txt                  # Python Dependencies
├── README.md                         # Complete Documentation & Usage Guide
└── VIVA_QUESTIONS_AND_ANSWERS.md     # 26-Question Viva Examination Preparation
```

---

## 🎓 Academic Viva Voce Preparation
For oral examinations and project viva, review [`VIVA_QUESTIONS_AND_ANSWERS.md`](file:///c:/Users/Arjun/OneDrive/Desktop/cse396%20new/VIVA_QUESTIONS_AND_ANSWERS.md) which contains exhaustive answers to 26 core theoretical, algorithmic, and methodological questions.
