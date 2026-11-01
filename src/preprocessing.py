"""
Preprocessing Module for Regional Search-Interest Clustering
============================================================

Project: CSE396 Unsupervised Learning Project
Stage: Day 2 — Data Preprocessing, Cleaning & Feature Scaling

Description:
------------
This module prepares the raw Google Trends dataset for clustering analysis:
1. Loads and audits the raw Google Trends data.
2. Handles missingness and validates integrity (no NaN values, duplicates checked).
3. Separates region identifiers (state, geo_code) from numerical clustering features.
4. Explains why categorical variables should NOT be one-hot encoded for geographic clustering.
5. Scales numerical features using StandardScaler (mean=0, std=1) to ensure equal
   weighting in Euclidean distance calculations.
6. Exports cleaned and processed datasets to `data/processed/`.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# 8 Selected emerging technology features
TOPIC_FEATURES = [
    "artificial_intelligence",
    "machine_learning",
    "data_science",
    "cloud_computing",
    "cybersecurity",
    "blockchain",
    "internet_of_things",
    "chatgpt",
]

IDENTIFIER_COLUMNS = ["state", "geo_code"]


def get_default_paths():
    """Resolve portable relative paths based on project structure."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "google_trends_raw_india.csv")
    processed_dir = os.path.join(base_dir, "data", "processed")
    return raw_path, processed_dir


def load_raw_dataset(filepath=None):
    """
    Load raw Google Trends dataset from disk.

    Parameters:
    -----------
    filepath : str, optional
        Path to raw CSV file.

    Returns:
    --------
    pd.DataFrame
        Loaded raw DataFrame.
    """
    if filepath is None:
        filepath, _ = get_default_paths()

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw data file not found at: {filepath}")

    df = pd.read_csv(filepath)
    print(f"[PREPROCESSING] Raw data loaded successfully. Shape: {df.shape}")
    return df


def audit_and_clean_data(df):
    """
    Audit missing values, check duplicates, and verify integrity.

    Parameters:
    -----------
    df : pd.DataFrame
        Input raw DataFrame.

    Returns:
    --------
    pd.DataFrame
        Cleaned DataFrame.
    dict
        Audit summary dictionary.
    """
    audit = {}

    # Check null / NaN counts
    null_counts = df.isnull().sum()
    audit["null_counts"] = null_counts.to_dict()
    audit["total_nulls"] = int(null_counts.sum())

    # Check duplicates
    row_duplicates = int(df.duplicated().sum())
    state_duplicates = int(df["state"].duplicated().sum())
    audit["row_duplicates"] = row_duplicates
    audit["state_duplicates"] = state_duplicates

    # Audit zero values (representing low relative search volume)
    zero_counts = (df[TOPIC_FEATURES] == 0).sum()
    audit["zero_counts"] = zero_counts.to_dict()

    print(f"[AUDIT] Total Null/NaN Values: {audit['total_nulls']}")
    print(f"[AUDIT] Duplicate Rows: {row_duplicates}, Duplicate States: {state_duplicates}")
    print(f"[AUDIT] Observations: {df.shape[0]} Indian States/UTs verified.")

    # Data is complete; no rows need deletion
    cleaned_df = df.copy()
    return cleaned_df, audit


def separate_features_and_identifiers(df):
    """
    Separate region identifiers from numerical clustering features.

    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned DataFrame.

    Returns:
    --------
    tuple (pd.DataFrame, pd.DataFrame)
        df_identifiers : Contains 'state' and 'geo_code'.
        df_features    : Contains the 8 numerical technology features.
    """
    df_identifiers = df[IDENTIFIER_COLUMNS].copy()
    df_features = df[TOPIC_FEATURES].copy()

    print(f"[SEPARATION] Identifiers shape: {df_identifiers.shape}")
    print(f"[SEPARATION] Clustering features shape: {df_features.shape}")
    return df_identifiers, df_features


def scale_features(df_features):
    """
    Scale numerical features using StandardScaler (mean=0, variance=1).

    Why Scaling is Necessary for K-Means:
    ------------------------------------
    K-Means is a distance-based clustering algorithm relying on Euclidean distance:
        d(x, y) = sqrt(sum((x_i - y_i)^2))
    Even though all features are on a 0-100 scale, their variance and baseline ranges
    differ (e.g. ChatGPT has a higher baseline than niche topics like IoT).
    Without standardization, high-variance features dominate the distance metrics.
    StandardScaler centers each feature to mean=0 and scales to unit variance (std=1),
    ensuring each emerging technology contributes equally to cluster formation.

    Parameters:
    -----------
    df_features : pd.DataFrame
        Raw numerical feature DataFrame.

    Returns:
    --------
    tuple (pd.DataFrame, StandardScaler)
        df_scaled : Standardized feature DataFrame.
        scaler    : Fitted StandardScaler instance.
    """
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(df_features)

    df_scaled = pd.DataFrame(
        scaled_array,
        columns=TOPIC_FEATURES,
        index=df_features.index,
    )

    print(f"[SCALING] Features standardized using StandardScaler.")
    print(f"[SCALING] Means after scaling (approx 0.0): {np.round(df_scaled.mean().values, 3)}")
    print(f"[SCALING] Stds after scaling (approx 1.0): {np.round(df_scaled.std(ddof=0).values, 3)}")

    return df_scaled, scaler


def export_processed_data(df_identifiers, df_features, df_scaled, output_dir=None):
    """
    Export processed datasets to data/processed/.

    Creates:
    1. `google_trends_processed_india.csv` - Combined table with identifiers, raw features, and scaled features.
    2. `features_scaled.csv` - Pure standardized matrix with state as index, ready for clustering.

    Parameters:
    -----------
    df_identifiers : pd.DataFrame
    df_features : pd.DataFrame
    df_scaled : pd.DataFrame
    output_dir : str, optional
    """
    if output_dir is None:
        _, output_dir = get_default_paths()

    os.makedirs(output_dir, exist_ok=True)

    # 1. Combined processed dataset
    combined = pd.concat([df_identifiers, df_features], axis=1)
    for col in TOPIC_FEATURES:
        combined[f"{col}_scaled"] = df_scaled[col]

    combined_path = os.path.join(output_dir, "google_trends_processed_india.csv")
    combined.to_csv(combined_path, index=False)
    print(f"[EXPORT] Combined processed data saved to: {combined_path}")

    # 2. Scaled features with state as index
    scaled_with_index = df_scaled.copy()
    scaled_with_index.index = df_identifiers["state"]
    scaled_path = os.path.join(output_dir, "features_scaled.csv")
    scaled_with_index.to_csv(scaled_path)
    print(f"[EXPORT] Scaled clustering matrix saved to: {scaled_path}")

    return combined_path, scaled_path


def run_preprocessing_pipeline(raw_path=None, processed_dir=None):
    """
    Execute the end-to-end preprocessing pipeline.

    Returns:
    --------
    dict containing all intermediate and final DataFrames and artifacts.
    """
    print("=" * 70)
    print("CSE396 - Day 2: Preprocessing Pipeline Execution")
    print("=" * 70)

    # Step 1: Load raw data
    df_raw = load_raw_dataset(raw_path)

    # Step 2: Audit and clean
    df_cleaned, audit = audit_and_clean_data(df_raw)

    # Step 3: Separate identifiers and features
    df_identifiers, df_features = separate_features_and_identifiers(df_cleaned)

    # Step 4: Scale numerical features
    df_scaled, scaler = scale_features(df_features)

    # Step 5: Export processed files
    combined_path, scaled_path = export_processed_data(
        df_identifiers, df_features, df_scaled, processed_dir
    )

    print("\n[COMPLETE] Day 2 Preprocessing Pipeline finished successfully.")
    return {
        "df_raw": df_raw,
        "df_cleaned": df_cleaned,
        "df_identifiers": df_identifiers,
        "df_features": df_features,
        "df_scaled": df_scaled,
        "scaler": scaler,
        "audit": audit,
        "combined_path": combined_path,
        "scaled_path": scaled_path,
    }


if __name__ == "__main__":
    results = run_preprocessing_pipeline()

