"""
Session State Manager and Global Theming for Streamlit Application
==================================================================
Initializes session state defaults, manages dataset caching, and
injects professional styling (Navy blue, clean cards, subtle shadows).
"""

import streamlit as st
import pandas as pd
import numpy as np


def init_session_state():
    """Ensure all required session state variables exist with safe defaults."""
    defaults = {
        "raw_data": None,
        "metadata_log": None,
        "cleaned_data": None,
        "preprocessing_report": None,
        "df_unscaled": None,
        "df_scaled": None,
        "scaler": None,
        "feature_info": {},
        "selected_algo": "K-Means",
        "selected_k": 3,
        "labels": None,
        "clustering_metrics": None,
        "df_eval_kmeans": None,
        "df_eval_kmedians": None,
        "mean_ari": None,
        "df_stability": None,
        "recommendations": None,
        "is_demo_mode": False,
        "min_coverage_pct": 80.0,
    }

    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def apply_custom_css():
    """Inject professional styling matching government analytics portals."""
    st.markdown("""
        <style>
            /* Main container width and padding */
            .main .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                max-width: 1200px;
            }
            
            /* Professional Typography & Palette */
            h1, h2, h3 {
                color: #0f172a !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                font-weight: 700;
            }
            
            /* Metric cards styling */
            [data-testid="stMetric"] {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            [data-testid="stMetricValue"] {
                color: #1e40af !important;
                font-weight: 700 !important;
                font-size: 1.6rem !important;
            }
            [data-testid="stMetricLabel"] {
                color: #64748b !important;
                font-size: 0.8rem !important;
                font-weight: 600 !important;
                text-transform: uppercase;
            }
            
            /* Professional Banner Cards */
            .hero-card {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #ffffff;
                padding: 24px 28px;
                border-radius: 12px;
                margin-bottom: 24px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .hero-title {
                font-size: 22px;
                font-weight: 800;
                color: #ffffff !important;
                margin-bottom: 4px;
            }
            .hero-subtitle {
                font-size: 14px;
                color: #38bdf8;
                font-weight: 600;
                margin-bottom: 8px;
            }
            .hero-desc {
                font-size: 12.5px;
                color: #cbd5e1;
                line-height: 1.5;
            }

            /* Demo Mode Alert Banner */
            .demo-banner {
                background-color: #fef3c7;
                border-left: 4px solid #f59e0b;
                color: #92400e;
                padding: 10px 14px;
                border-radius: 4px;
                font-size: 13px;
                margin-bottom: 16px;
                font-weight: 500;
            }

            /* Safeguard Alert Banner */
            .safeguard-banner {
                background-color: #eff6ff;
                border-left: 4px solid #3b82f6;
                color: #1e40af;
                padding: 10px 14px;
                border-radius: 4px;
                font-size: 13px;
                margin-bottom: 16px;
            }

            /* Clean table formatting */
            .dataframe {
                font-size: 13px !important;
            }
        </style>
    """, unsafe_allow_html=True)


def display_demo_warning():
    """Display clearly labelled demonstration mode badge if active."""
    if st.session_state.get("is_demo_mode", False):
        st.markdown("""
            <div class="demo-banner">
                ⚠️ <strong>DEMONSTRATION MODE ACTIVE:</strong> Using synthetic weekly Google Trends data for interface testing only.
                Never present demonstration results as actual empirical tourism research findings.
            </div>
        """, unsafe_allow_html=True)


# Aliases for flexible naming across modules
inject_custom_css = apply_custom_css
