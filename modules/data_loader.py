"""
Data Loader & Parser Module for Google Trends Tourism Data
===========================================================
Handles multi-file CSV ingestion, header parsing, region/topic inference,
metadata tracking, and synthetic demonstration dataset generation.
"""

import os
import re
import io
import pandas as pd
import numpy as np
from datetime import datetime

VALID_TOPICS = [
    "Tourism",
    "Travel",
    "Beaches",
    "Hill stations",
    "Wildlife tourism",
    "Religious tourism",
]

TOPICS = VALID_TOPICS

INDIAN_REGIONS = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand",
    "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra",
    "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal"
]


def infer_metadata_from_filename(filename):
    """
    Intelligently infer region and topic from uploaded filename.
    e.g., 'kerala_beaches_trends.csv' -> ('Kerala', 'Beaches')
    """
    clean_name = os.path.splitext(filename)[0].replace("-", " ").replace("_", " ").lower()
    
    inferred_region = None
    for region in INDIAN_REGIONS:
        if region.lower() in clean_name:
            inferred_region = region
            break
            
    inferred_topic = None
    topic_keywords = {
        "Tourism": ["tourism"],
        "Travel": ["travel", "tourist"],
        "Beaches": ["beach", "beaches", "coastal"],
        "Hill stations": ["hill station", "hill stations", "mountain", "hills"],
        "Wildlife tourism": ["wildlife", "safari", "national park", "tiger"],
        "Religious tourism": ["religious", "pilgrimage", "temple", "spiritual"]
    }
    
    for topic, keywords in topic_keywords.items():
        if any(kw in clean_name for kw in keywords):
            inferred_topic = topic
            break

    return inferred_region, inferred_topic


def parse_google_trends_csv(file_bytes, filename):
    """
    Parse standard Google Trends exported CSV format.
    Handles metadata headers, '<1' values, and variable date columns.
    """
    text = file_bytes.decode("utf-8", errors="replace")
    lines = text.splitlines()
    
    # Locate actual table header row (usually contains 'Week' or 'Month' or 'Date' or 'Day')
    header_idx = -1
    for i, line in enumerate(lines[:15]):
        line_lower = line.lower()
        if any(col in line_lower for col in ["week", "date", "month", "day"]):
            header_idx = i
            break
            
    if header_idx == -1:
        raise ValueError(f"Could not locate date column in CSV file: '{filename}'")
        
    csv_stream = io.StringIO("\n".join(lines[header_idx:]))
    df = pd.read_csv(csv_stream)
    
    # Standardize date column
    date_col = df.columns[0]
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=["date"])
    
    # Value column (second column)
    if len(df.columns) < 2:
        raise ValueError(f"No search interest values found in CSV file: '{filename}'")
        
    val_col = df.columns[1]
    
    # Handle '<1' or string interest values
    df["interest"] = df[val_col].astype(str).str.strip()
    df["interest"] = df["interest"].replace("<1", "0.5")
    df["interest"] = pd.to_numeric(df["interest"], errors="coerce")
    df["interest"] = df["interest"].clip(lower=0.0, upper=100.0)
    
    df = df[["date", "interest"]].sort_values("date").reset_index(drop=True)
    return df


def consolidate_uploaded_files(uploaded_files, user_assignments):
    """
    Consolidate multiple uploaded Google Trends CSV files into the required
    standard format: date, region, topic, interest.
    
    Parameters:
    -----------
    uploaded_files : list of UploadedFile objects
    user_assignments : dict mapping filename to {'region': str, 'topic': str}
    """
    consolidated_records = []
    metadata_log = []
    
    for uf in uploaded_files:
        fn = uf.name
        assign = user_assignments.get(fn, {})
        region = assign.get("region")
        topic = assign.get("topic")
        
        if not region or not topic:
            continue
            
        try:
            bytes_data = uf.getvalue()
            df = parse_google_trends_csv(bytes_data, fn)
            
            df["region"] = region
            df["topic"] = topic
            
            consolidated_records.append(df[["date", "region", "topic", "interest"]])
            
            metadata_log.append({
                "original_filename": fn,
                "region": region,
                "topic": topic,
                "start_date": df["date"].min().strftime("%Y-%m-%d"),
                "end_date": df["date"].max().strftime("%Y-%m-%d"),
                "record_count": len(df),
                "search_property": "Web Search",
                "notes": "Parsed successfully"
            })
        except Exception as e:
            metadata_log.append({
                "original_filename": fn,
                "region": region,
                "topic": topic,
                "start_date": None,
                "end_date": None,
                "record_count": 0,
                "search_property": "Web Search",
                "notes": f"Error parsing: {str(e)}"
            })
            
    if not consolidated_records:
        return pd.DataFrame(columns=["date", "region", "topic", "interest"]), pd.DataFrame(metadata_log)
        
    final_df = pd.concat(consolidated_records, ignore_index=True)
    return final_df, pd.DataFrame(metadata_log)


def generate_synthetic_demo_dataset():
    """
    Generate a realistic synthetic Google Trends demonstration dataset for Indian tourism.
    Dates: Weekly from 2023-11-05 to 2026-11-01 (157 weeks).
    Regions: 24 prominent Indian states representing distinct tourism profiles.
    Topics: 6 tourism topics with realistic cyclical season patterns.
    
    IMPORTANT: This is strictly for demonstration and testing the UI workflow.
    """
    dates = pd.date_range(start="2023-11-05", end="2026-11-01", freq="W-SUN")
    n_weeks = len(dates)
    
    # 24 Representative States with defined tourism characteristics
    state_profiles = {
        # Coastal & Beach Tourist States (Winter Q4/Q1 Peak)
        "Goa": {"Beaches": 1.8, "Tourism": 1.5, "Travel": 1.2, "Hill stations": 0.2, "Wildlife tourism": 0.5, "Religious tourism": 0.4, "beach_phase": 0},
        "Kerala": {"Beaches": 1.5, "Tourism": 1.6, "Travel": 1.3, "Hill stations": 1.0, "Wildlife tourism": 1.2, "Religious tourism": 0.8, "beach_phase": 0},
        "Puducherry": {"Beaches": 1.4, "Tourism": 1.1, "Travel": 1.0, "Hill stations": 0.1, "Wildlife tourism": 0.2, "Religious tourism": 0.6, "beach_phase": 0},
        "Odisha": {"Beaches": 1.2, "Tourism": 0.9, "Travel": 0.8, "Hill stations": 0.3, "Wildlife tourism": 0.9, "Religious tourism": 1.5, "beach_phase": 0},

        # Mountain & Hill Station States (Summer Q2 Peak & Winter Snow)
        "Himachal Pradesh": {"Hill stations": 1.9, "Tourism": 1.4, "Travel": 1.2, "Beaches": 0.1, "Wildlife tourism": 0.7, "Religious tourism": 0.6, "hill_phase": np.pi/2},
        "Uttarakhand": {"Hill stations": 1.8, "Tourism": 1.4, "Travel": 1.1, "Beaches": 0.1, "Wildlife tourism": 1.1, "Religious tourism": 1.8, "hill_phase": np.pi/2},
        "Sikkim": {"Hill stations": 1.7, "Tourism": 1.2, "Travel": 1.0, "Beaches": 0.1, "Wildlife tourism": 0.8, "Religious tourism": 0.7, "hill_phase": np.pi/2},
        "Jammu and Kashmir": {"Hill stations": 1.8, "Tourism": 1.3, "Travel": 1.1, "Beaches": 0.1, "Wildlife tourism": 0.6, "Religious tourism": 1.2, "hill_phase": np.pi/2},
        "Meghalaya": {"Hill stations": 1.5, "Tourism": 1.1, "Travel": 0.9, "Beaches": 0.1, "Wildlife tourism": 0.8, "Religious tourism": 0.4, "hill_phase": np.pi/2},

        # Wildlife & Heritage States (National Park season Q4/Q1)
        "Madhya Pradesh": {"Wildlife tourism": 1.8, "Tourism": 1.1, "Travel": 0.9, "Hill stations": 0.4, "Beaches": 0.1, "Religious tourism": 1.3, "wild_phase": 0},
        "Assam": {"Wildlife tourism": 1.7, "Tourism": 1.0, "Travel": 0.8, "Hill stations": 0.6, "Beaches": 0.1, "Religious tourism": 0.7, "wild_phase": 0},
        "Rajasthan": {"Tourism": 1.7, "Travel": 1.4, "Wildlife tourism": 1.4, "Hill stations": 0.5, "Beaches": 0.1, "Religious tourism": 1.1, "wild_phase": 0},

        # Pilgrimage & Cultural Tourism States
        "Uttar Pradesh": {"Religious tourism": 1.9, "Tourism": 1.2, "Travel": 1.0, "Hill stations": 0.2, "Beaches": 0.1, "Wildlife tourism": 0.6, "relig_phase": np.pi},
        "Tamil Nadu": {"Religious tourism": 1.7, "Tourism": 1.3, "Travel": 1.2, "Hill stations": 1.0, "Beaches": 1.1, "Wildlife tourism": 0.7, "relig_phase": np.pi},
        "Bihar": {"Religious tourism": 1.6, "Tourism": 0.7, "Travel": 0.6, "Hill stations": 0.1, "Beaches": 0.1, "Wildlife tourism": 0.4, "relig_phase": np.pi},
        "Punjab": {"Religious tourism": 1.5, "Tourism": 0.9, "Travel": 0.8, "Hill stations": 0.3, "Beaches": 0.1, "Wildlife tourism": 0.3, "relig_phase": np.pi},

        # Urban & Commercial Hubs (Steady Corporate & Leisure Travel)
        "Maharashtra": {"Travel": 1.6, "Tourism": 1.4, "Hill stations": 1.1, "Beaches": 1.2, "Wildlife tourism": 1.0, "Religious tourism": 1.3, "gen_phase": 0},
        "Karnataka": {"Travel": 1.5, "Tourism": 1.4, "Hill stations": 1.2, "Beaches": 0.9, "Wildlife tourism": 1.3, "Religious tourism": 1.2, "gen_phase": 0},
        "Delhi": {"Travel": 1.7, "Tourism": 1.5, "Hill stations": 1.2, "Beaches": 0.4, "Wildlife tourism": 0.8, "Religious tourism": 0.9, "gen_phase": 0},
        "Gujarat": {"Travel": 1.3, "Tourism": 1.2, "Religious tourism": 1.4, "Wildlife tourism": 1.2, "Beaches": 0.8, "Hill stations": 0.3, "gen_phase": 0},
        "West Bengal": {"Tourism": 1.3, "Travel": 1.1, "Hill stations": 1.2, "Beaches": 1.0, "Wildlife tourism": 0.9, "Religious tourism": 1.1, "gen_phase": 0},
        "Andhra Pradesh": {"Religious tourism": 1.6, "Tourism": 1.0, "Travel": 0.9, "Hill stations": 0.4, "Beaches": 0.8, "Wildlife tourism": 0.5, "gen_phase": 0},
        "Telangana": {"Travel": 1.3, "Tourism": 1.1, "Religious tourism": 1.0, "Hill stations": 0.2, "Beaches": 0.2, "Wildlife tourism": 0.6, "gen_phase": 0},
        "Haryana": {"Travel": 1.1, "Tourism": 0.8, "Hill stations": 0.4, "Beaches": 0.1, "Wildlife tourism": 0.3, "Religious tourism": 0.8, "gen_phase": 0},
    }

    week_of_year = dates.isocalendar().week.values
    t_cycle = 2 * np.pi * week_of_year / 52.0
    
    records = []
    np.random.seed(42)

    for state, weights in state_profiles.items():
        for topic in VALID_TOPICS:
            weight = weights.get(topic, 0.5)
            
            # Base seasonal curves
            if topic == "Hill stations":
                # Peaks around May-June (weeks 18-24)
                seasonal = np.sin(t_cycle - 1.8)
            elif topic == "Beaches":
                # Peaks around Dec-Jan (weeks 48-4)
                seasonal = np.cos(t_cycle - 0.2)
            elif topic == "Wildlife tourism":
                # Peaks in open season Nov-March
                seasonal = np.cos(t_cycle - 0.4)
            elif topic == "Religious tourism":
                # Multi-seasonal peaks (festivals in autumn and spring)
                seasonal = 0.6 * np.sin(2 * t_cycle) + 0.4 * np.cos(t_cycle)
            else: # Tourism / Travel
                seasonal = 0.5 * np.cos(t_cycle - 0.2) + 0.5 * np.sin(t_cycle - 1.8)

            noise = np.random.normal(0, 0.15, size=n_weeks)
            trend = np.linspace(0, 0.1, n_weeks)
            
            raw_signal = (weight * (1.0 + 0.6 * seasonal) + trend + noise)
            
            # Scale to Google Trends (0 to 100)
            scaled_signal = np.interp(raw_signal, (raw_signal.min(), raw_signal.max()), (15, 95))
            scaled_signal = np.round(scaled_signal).astype(int)
            
            # Add small random zeros for low interest topics in specific regions
            if weight < 0.3:
                zero_mask = np.random.rand(n_weeks) < 0.15
                scaled_signal[zero_mask] = 0

            for d, val in zip(dates, scaled_signal):
                records.append({
                    "date": d.strftime("%Y-%m-%d"),
                    "region": state,
                    "topic": topic,
                    "interest": int(val)
                })

    df_demo = pd.DataFrame(records)
    return df_demo


generate_synthetic_demo_data = generate_synthetic_demo_dataset

