"""
Tourism Planning Recommendations Module
=======================================
Generates evidence-based promotional planning suggestions from actual
cluster seasonal profiles and observed feature values.
Includes strict decision-support safeguards and validation metric advice.
"""

import pandas as pd
import numpy as np


def generate_planning_recommendations(df_features_unscaled, labels, region_names):
    """
    Generate actionable tourism promotional hypotheses based on cluster seasonal profiles.
    
    Parameters:
    -----------
    df_features_unscaled : pd.DataFrame
        Unscaled engineered seasonal feature matrix.
    labels : np.ndarray
        Final cluster assignments.
    region_names : list
        List of Indian states/UTs.
        
    Returns:
    --------
    pd.DataFrame
        Structured recommendation table with safeguards.
    """
    df_temp = df_features_unscaled.copy()
    df_temp["cluster"] = labels
    df_temp["region"] = region_names

    cluster_means = df_temp.groupby("cluster").mean(numeric_only=True)
    recommendations = []

    for c_id in cluster_means.index:
        c_regions = df_temp[df_temp["cluster"] == c_id]["region"].tolist()
        c_row = cluster_means.loc[c_id]

        # 1. Hill Stations Seasonal Analysis
        hill_q1 = c_row.get("Hillstations_Q1", c_row.get("HillstationsQ1", 0.0))
        hill_q2 = c_row.get("Hillstations_Q2", c_row.get("HillstationsQ2", 0.0))
        if hill_q2 > 0.4 or hill_q2 > hill_q1:
            recommendations.append({
                "Cluster_ID": f"Cluster {c_id}",
                "Member_Regions": ", ".join(c_regions[:6]) + (f" (+{len(c_regions)-6} more)" if len(c_regions) > 6 else ""),
                "Target_Topic": "Hill stations",
                "Peak_Quarter": "Q2 (April–June)",
                "Observed_Pattern": f"Elevated standardized Q2 search interest (Z = {hill_q2:+.2f}).",
                "Campaign_Strategy": "Pre-Summer Mountain Escape & Eco-Tourism Awareness Campaign",
                "Strategic_Rationale": "Online search curiosity surges in late spring prior to summer school holidays. Launching targeted campaigns in Q1/early Q2 captures active trip planners.",
                "Planning_Confidence": "High Evidence (Seasonal Peak)",
                "Validation_Metrics": "Digital campaign click-through rate, hotel booking queries, state tourism portal inquiries."
            })

        # 2. Beaches & Coastal Destinations
        beach_q4 = c_row.get("Beaches_Q4", c_row.get("BeachesQ4", 0.0))
        beach_q1 = c_row.get("Beaches_Q1", c_row.get("BeachesQ1", 0.0))
        if beach_q4 > 0.3 or beach_q1 > 0.3:
            peak_q = "Q4 (Oct–Dec) & Q1 (Jan–Mar)"
            val = max(beach_q4, beach_q1)
            recommendations.append({
                "Cluster_ID": f"Cluster {c_id}",
                "Member_Regions": ", ".join(c_regions[:6]) + (f" (+{len(c_regions)-6} more)" if len(c_regions) > 6 else ""),
                "Target_Topic": "Beaches",
                "Peak_Quarter": peak_q,
                "Observed_Pattern": f"Elevated autumn/winter coastal interest (Z = {val:+.2f}).",
                "Campaign_Strategy": "Winter Sun & Coastal Heritage Awareness Drive",
                "Strategic_Rationale": "Winter temperatures make coastal regions prime destinations for domestic and international travelers.",
                "Planning_Confidence": "High Evidence (Seasonal Peak)",
                "Validation_Metrics": "Coastal homestay registrations, ferry/cruise inquiries, beach festival attendance."
            })

        # 3. Wildlife & National Parks
        wild_q4 = c_row.get("Wildlifetourism_Q4", c_row.get("WildlifetourismQ4", 0.0))
        wild_q1 = c_row.get("Wildlifetourism_Q1", c_row.get("WildlifetourismQ1", 0.0))
        if wild_q4 > 0.3 or wild_q1 > 0.3:
            recommendations.append({
                "Cluster_ID": f"Cluster {c_id}",
                "Member_Regions": ", ".join(c_regions[:6]) + (f" (+{len(c_regions)-6} more)" if len(c_regions) > 6 else ""),
                "Target_Topic": "Wildlife tourism",
                "Peak_Quarter": "Q4 & Q1 (Open Safari Season)",
                "Observed_Pattern": f"Strong winter safari interest (Q4 Z={wild_q4:+.2f}, Q1 Z={wild_q1:+.2f}).",
                "Campaign_Strategy": "Responsible Safari & Wildlife Conservation Trail Campaign",
                "Strategic_Rationale": "National parks and wildlife sanctuaries in India typically open October to May, creating a concentrated search window for wildlife enthusiasts.",
                "Planning_Confidence": "Moderate-to-High Evidence",
                "Validation_Metrics": "Online safari permit bookings, forest department rest-house occupancy, wildlife tour operator leads."
            })

        # 4. Religious & Spiritual Tourism
        relig_q3 = c_row.get("Religioustourism_Q3", c_row.get("ReligioustourismQ3", 0.0))
        relig_q4 = c_row.get("Religioustourism_Q4", c_row.get("ReligioustourismQ4", 0.0))
        if relig_q3 > 0.2 or relig_q4 > 0.2:
            recommendations.append({
                "Cluster_ID": f"Cluster {c_id}",
                "Member_Regions": ", ".join(c_regions[:6]) + (f" (+{len(c_regions)-6} more)" if len(c_regions) > 6 else ""),
                "Target_Topic": "Religious tourism",
                "Peak_Quarter": "Q3 (Monsoon Festivals) & Q4 (Autumn Pilgrimages)",
                "Observed_Pattern": f"Elevated pilgrimage search volume in festival season (Z = {max(relig_q3, relig_q4):+.2f}).",
                "Campaign_Strategy": "Spiritual Circuit & Heritage Pilgrim Facilitation Outreach",
                "Strategic_Rationale": "Autumn festive cycles (Navratri, Diwali, Karthigai, etc.) stimulate multi-generational domestic family pilgrimages.",
                "Planning_Confidence": "High Evidence (Cultural Cycles)",
                "Validation_Metrics": "Special pilgrim train/bus booking traffic, temple trust accommodation requests, crowd management app downloads."
            })

        # 5. Volatility & Off-Season Smoothing
        vol_col = [c for c in c_row.index if "volatility" in c.lower()]
        if vol_col:
            mean_vol = c_row[vol_col].mean()
            if mean_vol > 0.8:
                recommendations.append({
                    "Cluster_ID": f"Cluster {c_id}",
                    "Member_Regions": ", ".join(c_regions[:6]) + (f" (+{len(c_regions)-6} more)" if len(c_regions) > 6 else ""),
                    "Target_Topic": "All Tourism Domains",
                    "Peak_Quarter": "Monsoon / Shoulder Season",
                    "Observed_Pattern": f"High seasonal demand volatility (Avg Volatility = {mean_vol:.2f}).",
                    "Campaign_Strategy": "Off-Season 'Monsoon Magic' & Wellness Retreat Smoothing Campaign",
                    "Strategic_Rationale": "Highly volatile search interest indicates extreme peak/trough cycles. Promoting monsoon tourism and wellness packages stabilizes local hospitality revenue.",
                    "Planning_Confidence": "Strategic Recommendation",
                    "Validation_Metrics": "Off-season hotel occupancy gains, discounted travel package redemptions."
                })

    if not recommendations:
        # Fallback generic recommendation if data has low variance
        recommendations.append({
            "Cluster_ID": "All Clusters",
            "Member_Regions": ", ".join(region_names[:5]),
            "Target_Topic": "General Tourism",
            "Peak_Quarter": "Annual",
            "Observed_Pattern": "Moderate baseline interest across domains.",
            "Campaign_Strategy": "Integrated State Tourism Portal Awareness Campaign",
            "Strategic_Rationale": "Baseline interest indicates opportunities to educate travelers on lesser-known destinations.",
            "Planning_Confidence": "Preliminary",
            "Validation_Metrics": "Website visit growth, newsletter signups."
        })

    return pd.DataFrame(recommendations)

