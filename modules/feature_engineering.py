"""
Feature Engineering Module for Regional Tourism Demand Segmentation
===================================================================
Constructs a regional feature matrix (one row per Indian State/UT).
Extracts quarterly seasonal means, annual intensity, volatility, and
linear trend slopes for each tourism topic.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


def clean_topic_name(topic):
    """Generate clean prefix for column names."""
    return topic.replace(" ", "").replace("_", "").replace("-", "")


def compute_trend_slope(series):
    """Compute OLS linear slope across weekly observations."""
    n = len(series)
    if n < 3:
        return 0.0
    x = np.arange(n)
    y = series.values
    # Polyfit degree 1 gives slope
    slope, _ = np.polyfit(x, y, 1)
    return float(slope * 52.0)  # Annualized slope


def construct_regional_features(df_processed):
    """
    Construct the final regional clustering feature matrix from preprocessed weekly series.
    
    Parameters:
    -----------
    df_processed : pd.DataFrame
        Preprocessed DataFrame containing ['date', 'region', 'topic', 'standardized_interest']
        
    Returns:
    --------
    tuple (pd.DataFrame, pd.DataFrame, StandardScaler, dict)
        df_unscaled : Feature matrix with raw engineered values (Region as index)
        df_scaled   : Standardized feature matrix (StandardScaler applied)
        scaler      : Fitted StandardScaler instance
        feature_info: Dictionary describing each engineered feature
    """
    if df_processed.empty:
        return pd.DataFrame(), pd.DataFrame(), None, {}

    df = df_processed.copy()
    df["quarter"] = df["date"].dt.quarter  # 1, 2, 3, 4
    
    regions = sorted(df["region"].unique())
    topics = sorted(df["topic"].unique())

    regional_records = []
    feature_info = {}

    for r in regions:
        region_dict = {"region": r}
        sub_r = df[df["region"] == r]

        for t in topics:
            sub_rt = sub_r[sub_r["topic"] == t]
            prefix = clean_topic_name(t)

            if sub_rt.empty:
                # Will be imputed by median imputer later
                region_dict[f"{prefix}_Q1"] = np.nan
                region_dict[f"{prefix}_Q2"] = np.nan
                region_dict[f"{prefix}_Q3"] = np.nan
                region_dict[f"{prefix}_Q4"] = np.nan
                region_dict[f"{prefix}_AnnualAvg"] = np.nan
                region_dict[f"{prefix}_Volatility"] = np.nan
                region_dict[f"{prefix}_TrendSlope"] = np.nan
            else:
                # Quarterly seasonal averages of standardized interest
                q1_val = sub_rt[sub_rt["quarter"] == 1]["standardized_interest"].mean()
                q2_val = sub_rt[sub_rt["quarter"] == 2]["standardized_interest"].mean()
                q3_val = sub_rt[sub_rt["quarter"] == 3]["standardized_interest"].mean()
                q4_val = sub_rt[sub_rt["quarter"] == 4]["standardized_interest"].mean()
                ann_val = sub_rt["standardized_interest"].mean()
                vol_val = sub_rt["standardized_interest"].std()
                slope_val = compute_trend_slope(sub_rt.sort_values("date")["standardized_interest"])

                region_dict[f"{prefix}_Q1"] = float(q1_val) if not np.isnan(q1_val) else 0.0
                region_dict[f"{prefix}_Q2"] = float(q2_val) if not np.isnan(q2_val) else 0.0
                region_dict[f"{prefix}_Q3"] = float(q3_val) if not np.isnan(q3_val) else 0.0
                region_dict[f"{prefix}_Q4"] = float(q4_val) if not np.isnan(q4_val) else 0.0
                region_dict[f"{prefix}_AnnualAvg"] = float(ann_val) if not np.isnan(ann_val) else 0.0
                region_dict[f"{prefix}_Volatility"] = float(vol_val) if not np.isnan(vol_val) else 0.0
                region_dict[f"{prefix}_TrendSlope"] = float(slope_val)

            # Document feature descriptions once
            if f"{prefix}_Q1" not in feature_info:
                feature_info[f"{prefix}_Q1"] = f"{t}: Average Q1 (Jan–Mar) standardized interest."
                feature_info[f"{prefix}_Q2"] = f"{t}: Average Q2 (Apr–Jun) standardized interest."
                feature_info[f"{prefix}_Q3"] = f"{t}: Average Q3 (Jul–Sep) standardized interest."
                feature_info[f"{prefix}_Q4"] = f"{t}: Average Q4 (Oct–Dec) standardized interest."
                feature_info[f"{prefix}_AnnualAvg"] = f"{t}: Overall mean standardized interest."
                feature_info[f"{prefix}_Volatility"] = f"{t}: Standard deviation of weekly interest (demand volatility)."
                feature_info[f"{prefix}_TrendSlope"] = f"{t}: Annualized OLS growth slope over the 3-year period."

        regional_records.append(region_dict)

    df_features = pd.DataFrame(regional_records).set_index("region")

    # Handle any remaining missingness via median imputation
    imputer = SimpleImputer(strategy="median")
    imputed_values = imputer.fit_transform(df_features)
    df_unscaled = pd.DataFrame(imputed_values, columns=df_features.columns, index=df_features.index)

    # Scale using StandardScaler across all regions
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(df_unscaled)
    df_scaled = pd.DataFrame(scaled_values, columns=df_unscaled.columns, index=df_unscaled.index)

    return df_unscaled, df_scaled, scaler, feature_info

