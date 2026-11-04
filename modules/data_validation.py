"""
Data Validation Module for Google Trends Tourism Data
======================================================
Validates required columns, ranges, duplicates, missing weeks,
and computes regional data coverage percentages.
"""

import pandas as pd
import numpy as np


def validate_raw_dataset(df, expected_freq="W-SUN", min_coverage_pct=80.0):
    """
    Perform rigorous data validation on consolidated Google Trends dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Consolidated dataset with columns ['date', 'region', 'topic', 'interest']
    expected_freq : str
        Weekly frequency identifier.
    min_coverage_pct : float
        Minimum percentage of weeks required for an eligible region.
        
    Returns:
    --------
    dict
        Comprehensive validation audit and summary statistics.
    pd.DataFrame
        Coverage report per region and topic.
    """
    audit = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "total_records": len(df),
        "unique_regions": 0,
        "unique_topics": 0,
        "date_min": None,
        "date_max": None,
        "duplicate_count": 0,
        "null_count": 0,
        "out_of_range_count": 0,
        "zero_count": 0,
        "eligible_regions_count": 0,
    }

    # Check required columns
    required_cols = {"date", "region", "topic", "interest"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        audit["is_valid"] = False
        audit["errors"].append(f"Missing required columns: {list(missing_cols)}")
        return audit, pd.DataFrame()

    if df.empty:
        audit["is_valid"] = False
        audit["errors"].append("Uploaded dataset is empty.")
        return audit, pd.DataFrame()

    df_val = df.copy()
    
    # 1. Date parsing
    df_val["parsed_date"] = pd.to_datetime(df_val["date"], errors="coerce")
    invalid_dates = df_val["parsed_date"].isnull().sum()
    if invalid_dates > 0:
        audit["errors"].append(f"Found {invalid_dates} invalid or unparseable date entries.")
        audit["is_valid"] = False

    audit["date_min"] = df_val["parsed_date"].min().strftime("%Y-%m-%d") if not df_val["parsed_date"].isnull().all() else None
    audit["date_max"] = df_val["parsed_date"].max().strftime("%Y-%m-%d") if not df_val["parsed_date"].isnull().all() else None

    # 2. Duplicate audit
    duplicates = df_val.duplicated(subset=["parsed_date", "region", "topic"]).sum()
    audit["duplicate_count"] = int(duplicates)
    if duplicates > 0:
        audit["warnings"].append(f"Found {duplicates} duplicate (date, region, topic) observations.")

    # 3. Numeric interest validation
    df_val["num_interest"] = pd.to_numeric(df_val["interest"], errors="coerce")
    null_interests = df_val["num_interest"].isnull().sum()
    audit["null_count"] = int(null_interests)
    if null_interests > 0:
        audit["warnings"].append(f"Found {null_interests} non-numeric or missing interest values.")

    # Out of range values (< 0 or > 100)
    out_of_bounds = ((df_val["num_interest"] < 0) | (df_val["num_interest"] > 100)).sum()
    audit["out_of_range_count"] = int(out_of_bounds)
    if out_of_bounds > 0:
        audit["errors"].append(f"Found {out_of_bounds} interest values outside valid 0–100 scale.")
        audit["is_valid"] = False

    # Zero values
    zeros = (df_val["num_interest"] == 0).sum()
    audit["zero_count"] = int(zeros)

    # 4. Regional and topic coverage calculation
    audit["unique_regions"] = int(df_val["region"].nunique())
    audit["unique_topics"] = int(df_val["topic"].nunique())

    # Calculate expected full calendar weeks between global min and max dates
    if audit["date_min"] and audit["date_max"]:
        calendar_weeks = pd.date_range(start=audit["date_min"], end=audit["date_max"], freq=expected_freq)
        expected_n_weeks = max(1, len(calendar_weeks))
    else:
        expected_n_weeks = 1

    # Regional coverage analysis
    coverage_rows = []
    regions = df_val["region"].dropna().unique()
    topics = df_val["topic"].dropna().unique()

    for r in regions:
        region_df = df_val[df_val["region"] == r]
        total_obs = len(region_df)
        topic_count = region_df["topic"].nunique()
        
        # Coverage across all topics
        expected_region_obs = expected_n_weeks * len(topics)
        coverage_pct = round((total_obs / max(1, expected_region_obs)) * 100.0, 1)
        coverage_pct = min(100.0, coverage_pct)
        
        is_eligible = (coverage_pct >= min_coverage_pct) and (topic_count >= max(1, len(topics) * 0.5))

        coverage_rows.append({
            "region": r,
            "observations": total_obs,
            "topics_covered": f"{topic_count} / {len(topics)}",
            "coverage_percentage": coverage_pct,
            "status": "PASS" if is_eligible else "LOW_COVERAGE",
            "eligible": is_eligible
        })

    df_coverage = pd.DataFrame(coverage_rows).sort_values("coverage_percentage", ascending=False)
    audit["eligible_regions_count"] = int(df_coverage["eligible"].sum())

    if audit["eligible_regions_count"] < 2:
        audit["warnings"].append("Fewer than 2 eligible regions meet the minimum coverage threshold.")

    return audit, df_coverage

