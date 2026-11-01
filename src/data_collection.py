"""
Data Collection Module for Regional Search-Interest Pattern Segmentation
========================================================================

Project: CSE396 Unsupervised Learning Project
Title: Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering

Description:
------------
This module automates the retrieval of open Google Trends data across Indian
states and Union Territories for selected emerging technology topics.

Topics Selected (8 Topics):
---------------------------
1. Artificial Intelligence
2. Machine Learning
3. Data Science
4. Cloud Computing
5. Cybersecurity
6. Blockchain
7. Internet of Things
8. ChatGPT

Methodological Notes on Google Trends Regional Data:
---------------------------------------------------
- Scope: India (geo='IN'), regional resolution ('REGION') covering 36 states and UTs.
- Timeframe: Past 12 months ('today 12-m').
- Normalization: In Google Trends regional queries, search interest is indexed
  from 0 to 100 relative to the region with the highest proportion of searches
  for that specific query term within the designated timeframe and geography.
- Zero or low values indicate low query volume or minimal relative interest.
- These numbers represent search interest patterns on Google, NOT population-level
  knowledge, technical competence, or digital adoption.
"""

import os
import time
import pandas as pd
from pytrends.request import TrendReq

# Selected technology topics
SELECTED_TOPICS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Cloud Computing",
    "Cybersecurity",
    "Blockchain",
    "Internet of Things",
    "ChatGPT",
]

# Standard column name mapping for clean tabular analysis
COLUMN_MAPPING = {
    "geoName": "state",
    "geoCode": "geo_code",
    "Artificial Intelligence": "artificial_intelligence",
    "Machine Learning": "machine_learning",
    "Data Science": "data_science",
    "Cloud Computing": "cloud_computing",
    "Cybersecurity": "cybersecurity",
    "Blockchain": "blockchain",
    "Internet of Things": "internet_of_things",
    "ChatGPT": "chatgpt",
}


def fetch_regional_trends(
    topics=None,
    geo="IN",
    timeframe="today 12-m",
    request_delay=2,
    retries=3,
):
    """
    Fetch regional search interest from Google Trends for specified topics across Indian regions.

    Parameters:
    -----------
    topics : list of str, optional
        List of topic keywords to query. Defaults to SELECTED_TOPICS.
    geo : str, optional
        Two-letter ISO country code. Defaults to 'IN' (India).
    timeframe : str, optional
        Google Trends timeframe format. Defaults to 'today 12-m' (past 12 months).
    request_delay : int, optional
        Seconds to pause between requests to respect rate limits. Defaults to 2.
    retries : int, optional
        Number of retry attempts if a request encounters a transient network issue.

    Returns:
    --------
    pd.DataFrame
        Raw DataFrame containing state names, geo codes, and regional search interest scores.
    """
    if topics is None:
        topics = SELECTED_TOPICS

    print(f"Connecting to Google Trends API (geo={geo}, timeframe='{timeframe}')...")
    pytrend = TrendReq(hl="en-US", tz=330, timeout=(10, 30))

    topic_series_dict = {}
    geo_codes = None

    for idx, topic in enumerate(topics, start=1):
        success = False
        print(f"[{idx}/{len(topics)}] Querying topic: '{topic}'...")

        for attempt in range(1, retries + 1):
            try:
                pytrend.build_payload(
                    kw_list=[topic],
                    cat=0,
                    timeframe=timeframe,
                    geo=geo,
                    gprop="",
                )
                df_topic = pytrend.interest_by_region(
                    resolution="REGION",
                    inc_low_vol=True,
                    inc_geo_code=True,
                )

                if df_topic is not None and not df_topic.empty:
                    topic_series_dict[topic] = df_topic[topic]
                    if geo_codes is None and "geoCode" in df_topic.columns:
                        geo_codes = df_topic["geoCode"]
                    success = True
                    break
                else:
                    print(f"  Warning: Empty response for '{topic}'. Retrying ({attempt}/{retries})...")
            except Exception as e:
                print(f"  Attempt {attempt}/{retries} failed for '{topic}': {e}")
                time.sleep(request_delay * 2)

        if not success:
            raise RuntimeError(
                f"Failed to retrieve Google Trends data for topic '{topic}' after {retries} attempts."
            )

        time.sleep(request_delay)

    # Combine into a structured DataFrame
    combined_df = pd.DataFrame(topic_series_dict)
    combined_df.insert(0, "geoCode", geo_codes)
    combined_df.reset_index(inplace=True)  # geoName becomes a column

    # Rename columns to standardized identifiers
    combined_df.rename(columns=COLUMN_MAPPING, inplace=True)

    print(f"\nData collection complete. Shape: {combined_df.shape} (36 Indian States/UTs x {combined_df.shape[1]} features).")
    return combined_df


def save_raw_data(df, output_path=None):
    """
    Save the collected raw Google Trends dataset to a CSV file.

    Parameters:
    -----------
    df : pd.DataFrame
        Collected raw DataFrame.
    output_path : str, optional
        Destination file path. Defaults to 'data/raw/google_trends_raw_india.csv'.
    """
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "data", "raw", "google_trends_raw_india.csv")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Raw data successfully saved to: {output_path}")


def load_raw_data(data_path=None):
    """
    Load raw Google Trends dataset from disk.

    Parameters:
    -----------
    data_path : str, optional
        Path to raw CSV file. Defaults to 'data/raw/google_trends_raw_india.csv'.

    Returns:
    --------
    pd.DataFrame
        Loaded raw DataFrame.
    """
    if data_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "raw", "google_trends_raw_india.csv")

    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Raw data file not found at '{data_path}'. Run data collection first."
        )

    df = pd.read_csv(data_path)
    return df


if __name__ == "__main__":
    print("=" * 70)
    print("CSE396 - Day 1: Google Trends Data Collection")
    print("=" * 70)
    raw_df = fetch_regional_trends()
    save_raw_data(raw_df)
    print("\nVerifying reload of saved CSV:")
    verified_df = load_raw_data()
    print(f"Reload verified! Records: {verified_df.shape[0]}, Columns: {verified_df.shape[1]}")
    print(verified_df.head())

