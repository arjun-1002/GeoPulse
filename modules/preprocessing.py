"""
Preprocessing Module for Regional Google Trends Tourism Data
============================================================
Handles calendar alignment, deduplication, short-gap interpolation (<=2 weeks),
zero-value flagging, and internal series standardization for seasonal pattern analysis.
"""

import pandas as pd
import numpy as np


def preprocess_tourism_data(df, min_coverage_pct=80.0, max_gap_weeks=2):
    """
    Execute full preprocessing pipeline for Google Trends time series.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input consolidated dataset with ['date', 'region', 'topic', 'interest']
    min_coverage_pct : float
        Minimum required weekly coverage percentage to keep a region.
    max_gap_weeks : int
        Maximum consecutive missing weeks permitted for linear interpolation.
        
    Returns:
    --------
    pd.DataFrame
        Cleaned, aligned, and standardized dataset.
    dict
        Comprehensive preprocessing log & metrics.
    """
    report = {
        "original_records": len(df),
        "duplicates_removed": 0,
        "invalid_records_removed": 0,
        "short_gaps_interpolated": 0,
        "zeros_preserved": 0,
        "eligible_regions": [],
        "excluded_regions": [],
        "final_records": 0,
    }

    if df.empty:
        return pd.DataFrame(), report

    df_clean = df.copy()

    # 1. Parse dates and numeric interest
    df_clean["date"] = pd.to_datetime(df_clean["date"], errors="coerce")
    df_clean["interest"] = pd.to_numeric(df_clean["interest"], errors="coerce")
    df_clean = df_clean.dropna(subset=["date", "interest", "region", "topic"])

    # Range constraint
    df_clean["interest"] = df_clean["interest"].clip(lower=0.0, upper=100.0)

    # Deduplication (keep first or mean of duplicates)
    init_len = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=["date", "region", "topic"])
    report["duplicates_removed"] = init_len - len(df_clean)

    # Flag original zeros
    df_clean["is_zero"] = (df_clean["interest"] == 0)
    report["zeros_preserved"] = int(df_clean["is_zero"].sum())

    # 2. Determine global weekly calendar
    min_date = df_clean["date"].min()
    max_date = df_clean["date"].max()
    full_calendar = pd.date_range(start=min_date, end=max_date, freq="W-SUN")
    total_expected_weeks = len(full_calendar)

    # 3. Filter regions by coverage
    region_counts = df_clean.groupby("region")["date"].nunique()
    coverage_series = (region_counts / total_expected_weeks) * 100.0

    eligible_regions = coverage_series[coverage_series >= min_coverage_pct].index.tolist()
    excluded_regions = coverage_series[coverage_series < min_coverage_pct].index.tolist()

    report["eligible_regions"] = eligible_regions
    report["excluded_regions"] = excluded_regions

    if not eligible_regions:
        return pd.DataFrame(), report

    df_filtered = df_clean[df_clean["region"].isin(eligible_regions)].copy()

    # 4. Weekly calendar alignment & short gap interpolation per (region, topic)
    processed_series_list = []
    topics = df_filtered["topic"].unique()
    total_interpolated = 0

    for r in eligible_regions:
        for t in topics:
            sub = df_filtered[(df_filtered["region"] == r) & (df_filtered["topic"] == t)]
            if sub.empty:
                continue

            sub = sub.sort_values("date").set_index("date")
            
            # Reindex to uniform weekly calendar
            reindexed = sub.reindex(full_calendar)
            reindexed["region"] = r
            reindexed["topic"] = t

            # Count gaps before interpolation
            missing_mask = reindexed["interest"].isnull()
            
            # Interpolate only short gaps (limit=max_gap_weeks)
            reindexed["interest_interpolated"] = reindexed["interest"].interpolate(
                method="linear", limit=max_gap_weeks, limit_direction="forward"
            )
            
            # Flag which values were interpolated
            reindexed["is_interpolated"] = missing_mask & (~reindexed["interest_interpolated"].isnull())
            total_interpolated += int(reindexed["is_interpolated"].sum())

            # Use interpolated value if available, else drop if still missing
            reindexed["final_interest"] = reindexed["interest_interpolated"]
            reindexed = reindexed.dropna(subset=["final_interest"]).reset_index()
            reindexed = reindexed.rename(columns={"index": "date"})

            # 5. Internal Series Standardization
            # Formula: z = (interest - mean) / std (per region-topic series)
            s_mean = reindexed["final_interest"].mean()
            s_std = reindexed["final_interest"].std()

            if s_std > 1e-6:
                reindexed["standardized_interest"] = (reindexed["final_interest"] - s_mean) / s_std
            else:
                reindexed["standardized_interest"] = 0.0

            reindexed["interest"] = reindexed["final_interest"]
            reindexed["is_zero"] = (reindexed["interest"] == 0)

            keep_cols = ["date", "region", "topic", "interest", "standardized_interest", "is_interpolated", "is_zero"]
            processed_series_list.append(reindexed[keep_cols])

    report["short_gaps_interpolated"] = total_interpolated

    if not processed_series_list:
        return pd.DataFrame(), report

    df_processed = pd.concat(processed_series_list, ignore_index=True)
    report["final_records"] = len(df_processed)

    return df_processed, report

