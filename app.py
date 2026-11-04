"""
Root Application Entrypoint: Regional Tourism Promotion Planner
==============================================================
Official Project Title:
"Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering"

Subtitle:
"An AI-Powered Tourism Planning Support System for Indian States and Union Territories"

Course: CSE396 Unsupervised Learning
"""

import streamlit as st
from modules.state_manager import init_session_state, inject_custom_css

# Configure page metadata
st.set_page_config(
    page_title="Regional Tourism Promotion Planner | CSE396",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize persistent session states
init_session_state()
inject_custom_css()

# Configure Streamlit navigation
pages = {
    "Overview & Ingestion": [
        st.Page("pages/1_Home.py", title="Home Dashboard", icon="🏠", default=True),
        st.Page("pages/2_Data_Upload.py", title="Data Upload", icon="📥"),
    ],
    "Data Pipeline": [
        st.Page("pages/3_Preprocessing.py", title="Data Quality & Preprocessing", icon="🧹"),
        st.Page("pages/4_Feature_Engineering.py", title="Feature Engineering", icon="⚙️"),
    ],
    "Clustering & Exploration": [
        st.Page("pages/5_Clustering.py", title="Clustering Analysis", icon="🔬"),
        st.Page("pages/6_PCA_Visualization.py", title="PCA Visualization", icon="📊"),
        st.Page("pages/7_Cluster_Insights.py", title="Cluster Insights", icon="💡"),
    ],
    "Planning & Documentation": [
        st.Page("pages/8_Planning_Recommendations.py", title="Tourism Planning Recommendations", icon="🎯"),
        st.Page("pages/9_About.py", title="About the Project", icon="📖"),
    ]
}

pg = st.navigation(pages)

# Custom Sidebar Branding & Status Header
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 16px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 14px;">
            <div style="font-size: 11px; font-weight: 700; color: #0d9488; text-transform: uppercase; letter-spacing: 0.5px;">CSE396 Project</div>
            <div style="font-size: 16px; font-weight: 700; color: #1e3a8a; line-height: 1.25; margin-top: 4px;">Regional Tourism Promotion Planner</div>
            <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Indian States & UTs Clustering</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Active Dataset Status Badge
    if st.session_state.get("is_demo_mode", False):
        st.markdown(
            """
            <div style="background-color: #fef3c7; border: 1px solid #f59e0b; padding: 6px 10px; border-radius: 6px; font-size: 12px; color: #92400e; font-weight: 600; margin-bottom: 14px;">
                🧪 Demonstration Mode (Synthetic Data)
            </div>
            """,
            unsafe_allow_html=True
        )
    elif st.session_state.get("raw_data") is not None:
        st.markdown(
            """
            <div style="background-color: #d1fae5; border: 1px solid #10b981; padding: 6px 10px; border-radius: 6px; font-size: 12px; color: #065f46; font-weight: 600; margin-bottom: 14px;">
                🟢 Real Google Trends Data Loaded
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background-color: #f1f5f9; border: 1px solid #cbd5e1; padding: 6px 10px; border-radius: 6px; font-size: 12px; color: #475569; font-weight: 500; margin-bottom: 14px;">
                ⚪ No Dataset Active
            </div>
            """,
            unsafe_allow_html=True
        )

# Execute active page
pg.run()
