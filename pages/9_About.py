"""
Page 9: About the Project
=========================
Comprehensive academic documentation, methodology overview, research objectives,
algorithmic architecture, and ethical limitations.
"""

import streamlit as st
from modules.state_manager import init_session_state, inject_custom_css

init_session_state()
inject_custom_css()

st.title("9. About the Project & Academic Methodology")
st.markdown("### Official University Project Documentation — CSE396 Unsupervised Learning")

# Project Identity Banner
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%); color: white; padding: 26px; border-radius: 10px; margin-bottom: 25px;">
        <span style="background-color: #0d9488; color: white; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; letter-spacing: 0.5px;">CSE396 Course Project</span>
        <h2 style="color: white; margin-top: 10px; margin-bottom: 6px; font-size: 1.6rem;">Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering</h2>
        <div style="font-size: 1.05rem; color: #93c5fd; font-weight: 500;">Regional Tourism Promotion Planner</div>
        <div style="font-size: 0.9rem; color: #cbd5e1; margin-top: 4px;">An AI-Powered Tourism Planning Support System for Indian States and Union Territories</div>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4 = st.tabs(["🎯 Problem & Objectives", "🔬 Algorithmic Methodology", "🛡️ Ethical Safeguards & Limitations", "💻 System Architecture"])

with tab1:
    st.subheader("1. Problem Statement")
    st.markdown(
        """
        Different Indian states and union territories exhibit diverse, heterogeneous search-interest patterns 
        across tourism verticals (such as beaches, hill stations, wildlife sanctuaries, and pilgrimage circuits). 
        However, manually identifying cohesive regional segments across dozens of states and multiple years of weekly search 
        trends is methodologically challenging and prone to subjective bias.
        
        This project applies **unsupervised machine learning** to automatically group Indian states and union territories 
        that exhibit homogeneous search-interest profiles, providing an empirical basis for regional tourism promotion planning.
        """
    )
    
    st.subheader("2. Project Objectives")
    st.markdown(
        """
        1. **Systematic Ingestion:** Ingest multi-topic, multi-region Google Trends weekly time-series data for Indian states and UTs.
        2. **Methodological Preprocessing:** Align observations to a unified weekly Sunday calendar (`W-SUN`), interpolate isolated short gaps (≤ 2 weeks), preserve genuine zero values, and apply internal $Z$-score series standardization.
        3. **Feature Engineering:** Aggregate time series into 42 domain-specific indicators per region (Quarterly seasonal averages Q1–Q4, Annual baseline, Volatility, and OLS Trend Slope).
        4. **Dual Clustering Algorithms:** Implement standard **K-Means** (Euclidean $L_2$ distance) and a robust **K-Medians** algorithm (Manhattan $L_1$ distance with coordinate-wise median centroid updates).
        5. **Empirical Validation:** Rigorously evaluate cluster quality across candidate $K \in [2, 5]$ using within-cluster cost (Elbow method), Silhouette score, and Davies-Bouldin index.
        6. **Clustering Stability Testing:** Assess algorithmic stability across 10 random seeds using the Adjusted Rand Index (ARI).
        7. **Dimensionality Reduction & Profiling:** Project high-dimensional regional feature vectors onto 2D and 3D principal components (PCA) and construct seasonal radar fingerprints.
        8. **Evidence-Based Hypotheses:** Formulate seasonal tourism promotional campaign suggestions accompanied by confidence scores and field validation requirements.
        """
    )

with tab2:
    st.subheader("Clustering Algorithms: K-Means vs K-Medians")
    st.markdown(
        """
        | Dimension | K-Means Clustering | K-Medians Clustering |
        | :--- | :--- | :--- |
        | **Distance Metric** | Euclidean Distance ($L_2$ norm) | Manhattan Distance ($L_1$ norm) |
        | **Objective Function** | $\\min \\sum_{k} \\sum_{x \\in C_k} \\|x - \\mu_k\\|_2^2$ | $\\min \\sum_{k} \\sum_{x \\in C_k} \\|x - m_k\\|_1$ |
        | **Centroid Computation**| Coordinate-wise arithmetic mean $\\mu_k$ | Coordinate-wise median $m_k$ |
        | **Outlier Sensitivity**| Highly sensitive to extreme trend spikes | Robust against viral search spikes and skewed outliers |
        | **Use Case in Trends** | General spherical cluster discovery | Heavy-tailed regional search volume distributions |
        """
    )

    st.subheader("Feature Engineering Pipeline")
    st.markdown(
        """
        For each region and topic, weekly standardized values $z_{t}$ are transformed into 7 features:
        - **$Q_1$ Seasonal Mean:** Average standardized interest during January, February, and March.
        - **$Q_2$ Seasonal Mean:** Average standardized interest during April, May, and June.
        - **$Q_3$ Seasonal Mean:** Average standardized interest during July, August, and September.
        - **$Q_4$ Seasonal Mean:** Average standardized interest during October, November, and December.
        - **Annual Baseline:** Mean search interest over the full temporal window.
        - **Seasonal Volatility:** Standard deviation $\\sigma$ across weeks, capturing cyclicality.
        - **Temporal Trend Slope:** Ordinary Least Squares (OLS) regression slope $\\beta_1$ indicating whether interest is growing or declining.
        """
    )

with tab3:
    st.subheader("Critical Limitations and Ethical Safeguards")
    st.error(
        """
        ### ⚠️ Mandatory Interpretation Rules
        
        1. **Curiosity ≠ Economic Behavior or Footfall:** Google Trends measures relative search volume on Google Web Search. It does NOT measure physical tourist arrivals, hotel bookings, ticket purchases, tourist expenditure, or destination popularity among non-digital demographics.
        2. **Digital Divide & Regional Internet Penetration:** Regions with lower smartphone or internet penetration will produce lower absolute query counts. Because Google Trends normalizes by total regional query volume, results represent topic interest relative to that region's total search queries, NOT population-wide interest.
        3. **Demonstration Dataset Notice:** When running in Demonstration Mode, all clustering results, charts, and recommendations stem from synthetic simulated data. They must never be cited as real empirical research findings.
        4. **Pre-Implementation Field Verification:** Government planners and tourism departments must validate all algorithmic suggestions using official statistics:
           - State Department of Tourism footfall counts
           - Ministry of Tourism (India) domestic & foreign visitor statistics
           - Airport Authority of India (AAI) passenger traffic reports
           - Federation of Hotel & Restaurant Associations of India (FHRAI) occupancy surveys
        """
    )

with tab4:
    st.subheader("System Technology Stack")
    st.markdown(
        """
        - **Framework:** Streamlit (Multi-page Architecture)
        - **Data Processing:** Pandas, NumPy, SciPy
        - **Machine Learning:** Scikit-learn (`KMeans`, `StandardScaler`, `PCA`, `silhouette_score`, `davies_bouldin_score`, `adjusted_rand_score`)
        - **Interactive Graphics:** Plotly Graph Objects & Plotly Express
        - **Deployment Target:** Local Windows / Linux Python 3.10+ Environment
        """
    )
    
    st.subheader("Project Structure")
    st.code(
        """
cse396 new/
├── app.py                      # Root Streamlit Application Entrypoint
├── pages/
│   ├── 1_Home.py               # Home Executive Dashboard
│   ├── 2_Data_Upload.py        # Google Trends Multi-CSV Uploader
│   ├── 3_Preprocessing.py      # Quality Audit & Preprocessing Pipeline
│   ├── 4_Feature_Engineering.py# Regional Matrix Construction
│   ├── 5_Clustering.py         # K-Means & K-Medians Clustering Engine
│   ├── 6_PCA_Visualization.py  # 2D & 3D Interactive Dimensionality Reduction
│   ├── 7_Cluster_Insights.py   # Membership Directories & Radar Profiles
│   ├── 8_Planning_Recommendations.py # Evidence-Based Strategic Planning
│   └── 9_About.py              # Academic Documentation & Methodology
├── modules/
│   ├── data_loader.py          # Google Trends Ingestion & Demo Generator
│   ├── data_validation.py      # Schema, Boundary, and Quality Validation
│   ├── preprocessing.py        # Calendar Alignment & Standardization
│   ├── feature_engineering.py  # 42 Seasonal Regional Indicators
│   ├── clustering.py           # K-Means & Custom Manhattan K-Medians
│   ├── visualization.py        # Plotly Visualizations (PCA, Elbow, Radar)
│   ├── recommendations.py      # Promotional Hypotheses Generator
│   ├── report_generator.py     # HTML Executive Report Builder
│   └── state_manager.py        # Session State & Theme Management
├── requirements.txt            # Python Dependencies
└── README.md                   # Complete Setup & Academic Guide
        """,
        language="text"
    )

st.markdown("---")
st.success("✅ **CSE396 Academic Project Implementation Complete.**")

