# Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering

**Course:** CSE396 — Unsupervised Learning  
**Project Mode:** 4-Day Progressive Development  
**Current Status:** Day 2 Completed (Data Preprocessing, Feature Scaling & Exploratory Data Analysis)  

---

## 1. Project Overview & Real-Life Problem

### Problem Statement
> *"Different geographic regions may have distinct patterns of information demand and search interest in emerging technologies, but manually identifying meaningful groups across many regions and technology topics is difficult."*

This project applies unsupervised machine learning—specifically **K-Means Clustering**—to automatically partition Indian states and Union Territories into natural clusters based on their Google search-interest patterns across key emerging technology domains.

### Real-Life Applications
- **Curriculum & Technology Education Planning:** Identifying regions with emerging curiosity in AI, Data Science, or Cloud Computing to tailor specialized educational programs.
- **Skill-Development & Workshop Roadmaps:** Assisting academic institutions, state tech councils, and non-profits in directing technology bootcamps and awareness initiatives where interest is rising.
- **Regional Information-Demand Research:** Providing empirical evidence of spatial variations in emerging technology curiosity across India.

### Crucial Interpretation Rule (Non-Discriminatory / Non-Stereotyping Safeguard)
> **IMPORTANT ETHICAL SAFEGUARD:**  
> Google Trends search interest measures **relative search query volume on Google**, NOT actual knowledge, technological intelligence, education level, human competence, or adoption rate.
> - **Never state:** *"Region X has poor AI knowledge or low technical ability."*
> - **Correct framing:** *"Region X showed relatively lower Google search interest for the selected AI-related search terms during the analyzed 12-month period."*  
> Clusters represent patterns in aggregated search activity, never the inherent qualities or abilities of the people residing in those regions.

---

## 2. Why Unsupervised Learning?
The regional Google Trends dataset contains no predefined labels or ground-truth classifications indicating which state belongs to which technology cluster. Unsupervised clustering allows the algorithm to discover natural groupings based on multidimensional geometric proximity across search-interest profiles.

---

## 3. Dataset Scope & Selected Topics

- **Source:** Open Google Trends data collected via `pytrends` (official Google Trends endpoints).
- **Geographic Scope:** India (`geo='IN'`), state/UT resolution (`resolution='REGION'`) covering all **36 States and Union Territories**.
- **Time Range:** Past 12 Months (`today 12-m`), capturing sustained annual search curiosity.
- **Unit of Observation:** Each row represents one Indian State or Union Territory.
- **Selected Emerging Technology Topics (8 Features):**
  1. `artificial_intelligence` (Artificial Intelligence)
  2. `machine_learning` (Machine Learning)
  3. `data_science` (Data Science)
  4. `cloud_computing` (Cloud Computing)
  5. `cybersecurity` (Cybersecurity)
  6. `blockchain` (Blockchain)
  7. `internet_of_things` (Internet of Things)
  8. `chatgpt` (ChatGPT)

---

## 4. Current Project Structure (Day 2)

```
cse396 new/
│
├── data/
│   ├── raw/
│   │   └── google_trends_raw_india.csv       # Raw Google Trends dataset (36 States/UTs x 10 cols)
│   └── processed/
│       ├── google_trends_processed_india.csv # Combined dataset (identifiers + raw + scaled features)
│       └── features_scaled.csv               # Standardized 36x8 matrix (state as index)
│
├── notebooks/
│   └── regional_search_clustering.ipynb      # Day 1 & Day 2 Notebook with executed outputs and plots
│
├── outputs/
│   ├── figures/
│   │   ├── topic_distributions.png           # Boxplots & jitter plots of search interest by topic
│   │   ├── state_tech_interest_comparison.png# Bar chart: Top 15 states by mean tech curiosity
│   │   └── topic_correlation_heatmap.png     # Heatmap: Pearson correlation between topics
│   └── results/                              # Output directory for Day 3 & Day 4 tables
│
├── src/
│   ├── data_collection.py                    # Automated Google Trends collection script
│   ├── preprocessing.py                      # Preprocessing, auditing, and StandardScaler pipeline
│   └── visualization.py                      # Reusable EDA and diagnostic visualization module
│
├── .gitignore                                # Git ignore rules for Python & Jupyter
├── requirements.txt                          # Project dependency specifications
└── README.md                                 # Project documentation & Day 2 status
```

---

## 5. Four-Day Progressive Development Plan

| Day | Focus Areas | Status |
| :--- | :--- | :---: |
| **Day 1** | Project Setup + Real Google Trends Collection + Initial Dataset Inspection | **COMPLETED** |
| **Day 2** | **Data Cleaning + Feature Scaling (`StandardScaler`) + Exploratory Data Analysis (EDA)** | **COMPLETED** |
| **Day 3** | K-Means Experiments ($K=2,3,4,5$) + Validation (WCSS, Silhouette, Davies-Bouldin) + PCA 2D Plot | Pending |
| **Day 4** | Cluster Profiling + Stability Analysis + Limitations, Ethics & Viva Preparation | Pending |

---

## 6. Day 2 Preprocessing & EDA Findings

### A. Data Cleaning & Integrity Audit
- **Null Values:** `0` (Zero missing entries across all 36 Indian states and union territories).
- **Duplicates:** `0` duplicate rows; all 36 state names and ISO geo codes are unique.
- **Zero Values:** Zero values occur only in small Union Territories (e.g., Andaman and Nicobar Islands) for specialized topics like `internet_of_things`, reflecting real low query volume on Google rather than data corruption. No artificial imputation or row dropping was needed.

### B. Separation of Region Identifiers
- `state` and `geo_code` were separated from numerical clustering features.
- **Categorical Encoding Decision:** Categorical encoding (e.g., One-Hot Encoding) was deliberately **avoided**. In clustering, states are observations, not predictor variables. One-hot encoding would make all states mutually orthogonal ($d = \sqrt{2}$), destroying geographic search similarity.

### C. Feature Scaling via `StandardScaler`
- **Why Scaling is Mandatory:** K-Means minimizes Within-Cluster Sum of Squares (WCSS) using Euclidean distance:
  $$d(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{j=1}^{d} (x_j - y_j)^2}$$
- Different topics have different variances and baseline levels (e.g., `chatgpt` mean $\approx 55.8$, min 26 vs. `blockchain` mean $\approx 40.8$, min 0). Without standardization, higher-variance features dominate Euclidean distance.
- `StandardScaler` centers each topic to $\mu = 0$ and scales to unit variance $\sigma = 1$, placing all 8 technology dimensions on an equal mathematical footing.

### D. Exploratory Data Analysis (EDA) Highlights
1. **Strong Core Technological Associations:**
   - Artificial Intelligence, Machine Learning, Data Science, and Cybersecurity show strong positive correlations ($r \approx 0.82 - 0.89$), indicating that regions with active software ecosystems search for these foundational technologies together.
2. **Distinct Generative AI & Hardware Patterns:**
   - `chatgpt` shows broader adoption across non-hub regions ($r = 0.54 - 0.74$ with developer topics).
   - `internet_of_things` has low correlation with `chatgpt` ($r = 0.26$), reflecting hardware/embedded systems interest that follows a distinct regional pattern.
3. **Leading States by Tech Search Intensity:**
   - Southern and Western IT hubs (Telangana, Karnataka, Andhra Pradesh, Maharashtra) and Delhi exhibit consistently higher relative search intensity across multiple topics.

---

## 7. How to Reproduce Day 2 Work

### 1. Run Preprocessing Pipeline
```bash
python src/preprocessing.py
```
*(Loads raw CSV, audits data, separates features, applies `StandardScaler`, and exports to `data/processed/`)*

### 2. Generate EDA Figures
```bash
python src/visualization.py
```
*(Saves distribution plots, state comparisons, and correlation heatmap to `outputs/figures/`)*

### 3. Run the Jupyter Notebook
```bash
python -m notebook notebooks/regional_search_clustering.ipynb
```
*(Execute all cells in order to see step-by-step code, tables, and embedded visualizations)*
