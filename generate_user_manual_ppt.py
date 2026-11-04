"""
Script to Generate Professional User Manual Presentation (PPTX)
===============================================================
Creates an executive-grade 13-slide PowerPoint user manual for:
"Regional Tourism Promotion Planner"
CSE396 Unsupervised Learning Course Project
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# 16:9 Widescreen dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette
NAVY_DARK = RGBColor(15, 23, 42)      # #0F172A
NAVY_PRIMARY = RGBColor(30, 58, 138)  # #1E3A8A
TEAL = RGBColor(13, 148, 136)         # #0D9488
SLATE_DARK = RGBColor(30, 41, 59)     # #1E293B
SLATE_MUTED = RGBColor(100, 116, 139) # #64748B
BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC
CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
BORDER_COLOR = RGBColor(226, 232, 240)# #E2E8F0
GOLD = RGBColor(217, 119, 6)          # #D97706
WHITE = RGBColor(255, 255, 255)


def add_header(slide, title_text, category_text="USER MANUAL & OPERATIONS GUIDE"):
    """Adds a standard executive header to a content slide."""
    # Category tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_text.upper()
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = TEAL

    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.7))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY

    # Accent divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_COLOR
    line.line.color.rgb = BORDER_COLOR

    # Footer
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.3))
    tf_f = footer_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Regional Tourism Promotion Planner • CSE396 Unsupervised Learning • User Manual"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = SLATE_MUTED


def add_card(slide, left, top, width, height, title, items, badge=""):
    """Adds a structured white container card with bullet items."""
    # Base card shape
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = BORDER_COLOR
    card.line.width = Pt(1)

    # Card title and content text
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True

    # Title
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY
    p_title.space_after = Pt(10)

    # Bullets
    for item in items:
        p = tf.add_paragraph()
        if isinstance(item, tuple):
            prefix, text = item
            run_pre = p.add_run()
            run_pre.text = prefix + " "
            run_pre.font.bold = True
            run_pre.font.size = Pt(11)
            run_pre.font.color.rgb = SLATE_DARK

            run_txt = p.add_run()
            run_txt.text = text
            run_txt.font.size = Pt(11)
            run_txt.font.color.rgb = SLATE_DARK
        else:
            run_txt = p.add_run()
            run_txt.text = item
            run_txt.font.size = Pt(11)
            run_txt.font.color.rgb = SLATE_DARK
        p.space_after = Pt(6)


def build_presentation(output_path="USER_MANUAL_REGIONAL_TOURISM_PLANNER.pptx"):
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: Title Slide (Dark Hero Style)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK
    bg1.line.fill.background()

    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(10.9), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "CSE396 UNSUPERVISED LEARNING • SYSTEM USER MANUAL"
    p_badge.font.size = Pt(12)
    p_badge.font.bold = True
    p_badge.font.color.rgb = TEAL
    p_badge.space_after = Pt(16)

    p_title = tf1.add_paragraph()
    p_title.text = "Regional Tourism Promotion Planner"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE
    p_title.space_after = Pt(12)

    p_sub = tf1.add_paragraph()
    p_sub.text = "An AI-Powered Tourism Planning Support System for Indian States and Union Territories"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(147, 197, 253)
    p_sub.space_after = Pt(20)

    p_official = tf1.add_paragraph()
    p_official.text = "Official Academic Project Title: \"Regional Search-Interest Pattern Segmentation Across Selected Topics Using Clustering\""
    p_official.font.size = Pt(12)
    p_official.font.italic = True
    p_official.font.color.rgb = RGBColor(203, 213, 225)
    p_official.space_after = Pt(24)

    p_author = tf1.add_paragraph()
    p_author.text = "Author: Arjun (B.Tech CSE)  •  Stack: Python, Streamlit, Scikit-learn, Plotly"
    p_author.font.size = Pt(13)
    p_author.font.bold = True
    p_author.font.color.rgb = WHITE

    # ==========================================
    # SLIDE 2: Project Overview & Core Goals
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. System Overview & The Real-Life Problem")

    add_card(slide2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "The Core Real-Life Problem",
        [
            ("The Challenge:", "Indian States & UTs exhibit complex, seasonal, and thematic variations in tourism interest across beaches, mountains, wildlife, and pilgrimages."),
            ("Manual Inefficiency:", "Manually analyzing 36 regional jurisdictions across multi-year weekly search logs is subjective, slow, and prone to human bias."),
            ("Unsupervised ML Role:", "Clustering automatically groups regions sharing similar seasonal information demand without requiring pre-existing ground-truth labels."),
            ("Primary Beneficiaries:", "Ministry of Tourism, State Tourism Development Corporations, marketing planners, and policy researchers.")
        ]
    )

    add_card(slide2, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Analyzed Topics & Geographical Scope",
        [
            ("Geographical Scope:", "All 36 Indian States and Union Territories with sufficient query coverage."),
            ("6 Core Tourism Topics:", "Tourism, Travel, Beaches, Hill stations, Wildlife tourism, Religious tourism."),
            ("Data Source:", "Weekly Google Trends Web Search indices (scaled 0–100 within each request series)."),
            ("Temporal Horizon:", "Multi-year weekly observations (Nov 2023 to Nov 2026, 157 continuous weeks)."),
            ("Target Deliverable:", "Evidence-based, seasonal promotional campaign hypotheses backed by mathematical validation.")
        ]
    )

    # ==========================================
    # SLIDE 3: System Prerequisites & Quick Launch
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Getting Started: Installation & Startup")

    add_card(slide3, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Installation & Local Setup",
        [
            ("Python Requirement:", "Python 3.10, 3.11, or 3.12 installed on Windows, macOS, or Linux."),
            ("Repository Setup:", "Navigate to the project root directory in PowerShell or Terminal:"),
            ("Terminal Command:", "cd \"cse396 new\""),
            ("Dependency Install:", "pip install -r requirements.txt"),
            ("Key Packages:", "streamlit, plotly, pandas, numpy, scikit-learn, scipy.")
        ]
    )

    add_card(slide3, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Launching the Dashboard UI",
        [
            ("Single Startup Command:", "streamlit run app.py"),
            ("Local Web Address:", "http://localhost:8501 (automatically opens in your browser)."),
            ("Multi-Page Navigation:", "Streamlit 1.66 sidebar allows seamless 1-click navigation across all 9 project modules."),
            ("Session State Persistence:", "All uploaded data, preprocessing caches, fitted clusters, and settings persist safely across page changes."),
            ("Headless Server Ready:", "Runs smoothly in background without external database or cloud requirements.")
        ]
    )

    # ==========================================
    # SLIDE 4: Application Architecture & 9 Modules
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Application Architecture & Sidebar Map")

    col_w = Inches(3.6)
    add_card(slide4, Inches(0.8), Inches(1.7), col_w, Inches(5.0),
        "Phase I: Ingestion & Prep",
        [
            ("1. Home Dashboard:", "Status metrics, project identity, and 1-click demonstration dataset loader."),
            ("2. Data Upload:", "Drag-and-drop CSV uploader, metadata inference, and preview table."),
            ("3. Preprocessing:", "Calendar alignment (W-SUN), <=2 week gap interpolation, zero preservation, and Z-score normalization.")
        ]
    )

    add_card(slide4, Inches(4.8), Inches(1.7), col_w, Inches(5.0),
        "Phase II: Modeling & PCA",
        [
            ("4. Feature Engineering:", "Extracts 42 indicators (Q1-Q4 means, baseline, volatility, trend slope) per State/UT."),
            ("5. Clustering Analysis:", "K-Means (L2) vs K-Medians (L1), candidate K=2-5, Elbow plot, Silhouette, Davies-Bouldin, ARI stability."),
            ("6. PCA Visualization:", "Interactive 2D and 3D scatter projections with state tooltips and variance explained.")
        ]
    )

    add_card(slide4, Inches(8.8), Inches(1.7), col_w, Inches(5.0),
        "Phase III: Insights & Action",
        [
            ("7. Cluster Insights:", "State membership directories, seasonal radar fingerprints, and centroid profiles."),
            ("8. Planning Recommendations:", "Campaign suggestions, seasonal launch windows, validation metrics, and HTML report export."),
            ("9. About the Project:", "Academic problem statement, 8 research objectives, and ethical non-stereotyping safeguards.")
        ]
    )

    # ==========================================
    # SLIDE 5: Demonstration Mode vs Real Data
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Fast-Track Testing: Demonstration Mode")

    add_card(slide5, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Option A: 1-Click Demonstration Mode",
        [
            ("Instant Evaluation:", "Allows professors and evaluators to test the entire application without needing raw CSV files."),
            ("Synthetic Generation:", "Builds a realistic 24-state x 6-topic x 157-week dataset with authentic cyclical seasonality:"),
            ("Hill Stations:", "Prominent summer peaks in Q2 (May–June)."),
            ("Beaches:", "Winter sun surges in Q4 & Q1 (Nov–Feb)."),
            ("Wildlife Tourism:", "Synchronized with national park open seasons (Oct–March)."),
            ("Prominent Visual Badge:", "A yellow warning banner appears on all pages ensuring synthetic data is never confused with empirical research.")
        ]
    )

    add_card(slide5, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Option B: Real Google Trends Upload",
        [
            ("Multi-File Uploader:", "Accepts multiple standard CSV files exported directly from Google Trends."),
            ("Intelligent Metadata Parser:", "Automatically detects State and Topic from file names (e.g. 'kerala_beaches_trends.csv' -> Kerala, Beaches)."),
            ("Manual Override Form:", "Allows manual assignment of State and Topic if filenames are non-standard."),
            ("Consolidated DataFrame:", "Merges all files into a unified schema: ['date', 'region', 'topic', 'interest']."),
            ("Metadata Export:", "Download the parsing audit log as CSV for project documentation.")
        ]
    )

    # ==========================================
    # SLIDE 6: Preprocessing & Data Quality Pipeline
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Data Quality & Preprocessing Pipeline")

    add_card(slide6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Rigorous Time-Series Cleaning",
        [
            ("1. Weekly Calendar Alignment:", "Resamples all records to a consistent weekly Sunday cadence ('W-SUN')."),
            ("2. Short-Gap Linear Interpolation:", "Missing intervals of <=2 consecutive weeks are linearly interpolated to preserve series continuity."),
            ("3. Long-Gap Preservation:", "Gaps >2 weeks are left missing to prevent artificial distortion of trends."),
            ("4. Zero-Value Preservation:", "Distinguishes between missing data and genuine low-search weeks (e.g., beaches in non-coastal states)."),
            ("5. Coverage Threshold Filter:", "Excludes regions with <80% data completeness to ensure robust clustering.")
        ]
    )

    add_card(slide6, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Internal Series Standardization",
        [
            ("The Google Trends Challenge:", "Values (0–100) are relative only within each individual search query, preventing direct cross-topic comparison."),
            ("Mathematical Solution:", "Apply Z-score standardization within each regional topic series:"),
            ("Formula:", "Z = (X - μ) / σ"),
            ("Outcome:", "Centers baseline demand at 0 and measures quarterly fluctuations in standard deviation units."),
            ("Resulting Advantage:", "Allows the clustering algorithm to compare seasonal surge shapes rather than arbitrary baseline volume offsets.")
        ]
    )

    # ==========================================
    # SLIDE 7: Regional Feature Engineering Pipeline
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Regional Feature Matrix Construction")

    add_card(slide7, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Key Architectural Principle",
        [
            ("Unit of Observation:", "Clustering is performed at the REGIONAL level (one row per State/UT), NOT by clustering individual dates or weeks."),
            ("Goal:", "Characterize each state by its permanent multi-topic seasonal fingerprint."),
            ("Matrix Dimensions:", "N States/UTs (rows) x 42 Indicators (columns)."),
            ("Input Data:", "Standardized longitudinal weekly time-series observations."),
            ("StandardScaler:", "Features are passed through StandardScaler prior to distance computation to ensure equal feature weighting.")
        ]
    )

    add_card(slide7, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "7 Extracted Features Per Topic (42 Total)",
        [
            ("Q1 Seasonal Mean:", "Average standardized demand in Jan–Mar (Late Winter)."),
            ("Q2 Seasonal Mean:", "Average standardized demand in Apr–Jun (Summer)."),
            ("Q3 Seasonal Mean:", "Average standardized demand in Jul–Sep (Monsoon)."),
            ("Q4 Seasonal Mean:", "Average standardized demand in Oct–Dec (Autumn/Winter)."),
            ("Annual Mean Baseline:", "Overall central tendency over the full observation period."),
            ("Seasonal Volatility (σ):", "Standard deviation across weeks, capturing cyclicality."),
            ("OLS Trend Slope (β1):", "Linear annualized regression slope indicating multi-year demand growth or decline.")
        ]
    )

    # ==========================================
    # SLIDE 8: Dual Clustering Engine: K-Means vs K-Medians
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. Machine Learning Engine: K-Means vs K-Medians")

    add_card(slide8, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Standard K-Means (Euclidean L2)",
        [
            ("Distance Metric:", "Squared Euclidean Distance (L2 Norm)."),
            ("Optimization Objective:", "Minimizes within-cluster sum of squared errors (WCSS / Inertia)."),
            ("Centroid Computation:", "Coordinate-wise arithmetic mean μ_k."),
            ("Convergence:", "Lloyd's algorithm with n_init=50 random restarts and deterministic random_state=42."),
            ("Best Suited For:", "Normally distributed, spherical clusters without severe viral trend outliers.")
        ]
    )

    add_card(slide8, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Custom K-Medians (Manhattan L1)",
        [
            ("Distance Metric:", "Manhattan Absolute Distance (L1 Norm)."),
            ("Optimization Objective:", "Minimizes within-cluster sum of absolute differences."),
            ("Centroid Computation:", "Coordinate-wise MEDIAN m_k (mathematically optimal for L1)."),
            ("Outlier Robustness:", "Resistant to massive viral spikes and heavy-tailed search distributions."),
            ("Viva Insight:", "Proves candidate cluster stability across fundamental distance geometries.")
        ]
    )

    # ==========================================
    # SLIDE 9: Multi-Metric Model Validation
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. Multi-Metric Clustering Validation")

    add_card(slide9, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Model Selection Across Candidate K in [2, 5]",
        [
            ("Elbow Method Curve:", "Plots Within-Cluster Cost vs K. Identifies elbow point where additional clusters yield diminishing returns."),
            ("Silhouette Score (s):", "Measures cohesion vs separation (-1 to +1). Values >0.30 indicate defensible grouping structure."),
            ("Davies-Bouldin Index (DBI):", "Ratio of within-cluster scatter to between-cluster separation. Lower scores represent superior partitioning."),
            ("Defense Rationale:", "K=3 is methodologically optimal: marks the primary elbow inflection and produces actionable regional tiers without over-fragmentation.")
        ]
    )

    add_card(slide9, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Algorithmic Stability Testing (ARI)",
        [
            ("The Stability Problem:", "Centroid-based clustering can produce inconsistent results if initialized with different random seeds."),
            ("Testing Protocol:", "Models are re-fitted across 10 distinct random seeds (0, 7, 13, 21, 42, 77, 99, 123, 555, 999)."),
            ("Validation Metric:", "Adjusted Rand Index (ARI) comparing pairwise cluster partitions."),
            ("Result:", "Mean ARI > 0.90 confirms near-identical partitions across initializations, proving true underlying clusters rather than initialization artifacts.")
        ]
    )

    # ==========================================
    # SLIDE 10: Interactive PCA Visualizations
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "9. Dimensionality Reduction & PCA Exploration")

    add_card(slide10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Interactive 2D & 3D PCA Projections",
        [
            ("High-Dimensional Challenge:", "Humans cannot visualize 42 simultaneous seasonal dimensions."),
            ("PCA Solution:", "Linear orthogonal transformation projecting 42 features onto Principal Components (PC1, PC2, PC3)."),
            ("Variance Retention:", "PC1 and PC2 retain >80% of total information variance, ensuring geometric fidelity."),
            ("Interactive Plotly Graphics:", "Hover over any point to reveal the State name, cluster assignment, and exact PC coordinates."),
            ("3D Rotational Projection:", "Rotate the cluster sphere 360 degrees to verify visual spatial separation.")
        ]
    )

    add_card(slide10, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Crucial Methodology Safeguard",
        [
            ("VIVA DEFENSE POINT:", "Clustering was executed on the COMPLETE 42-dimensional standardized feature space, NOT on the reduced PCA components."),
            ("Why?:", "PCA is utilized purely as an ex-post visualization diagnostic, preserving all original variance during cluster optimization."),
            ("Component Loadings:", "PC1 captures general search enthusiasm and volume; PC2 separates mountain/summer interest from coastal/winter interest.")
        ]
    )

    # ==========================================
    # SLIDE 11: Cluster Insights & Radar Profiling
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "10. Cluster Profiling & Radar Fingerprints")

    add_card(slide11, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Cluster Membership & Characteristics",
        [
            ("Cluster 0: Mountain & Adventure Tier:", "Himachal Pradesh, Uttarakhand, Sikkim, J&K. Strong summer Q2 peaks in Hill stations, eco-tourism, and winter snow sports."),
            ("Cluster 1: Coastal & Winter Sun Tier:", "Goa, Kerala, Puducherry, Odisha, Tamil Nadu. Dominant Q4/Q1 peaks in beaches, coastal leisure, and water sports."),
            ("Cluster 2: Heritage & Wildlife Tier:", "Madhya Pradesh, Rajasthan, Assam, Uttar Pradesh. Autumn/winter safari interest and steady pilgrimage queries."),
            ("State Directory:", "Interactive dropdown allows instant inspection of any state's cluster assignment and peer group.")
        ]
    )

    add_card(slide11, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Seasonal Radar Fingerprints",
        [
            ("Radar Visualization:", "Plots standardized quarterly means (Q1–Q4) in a multi-axis radial chart."),
            ("Spike Interpretation:", "Radial points > 0 represent quarters where query volume significantly exceeds the state's annual baseline."),
            ("Visual Segmentation:", "Clearly demonstrates how different clusters have alternating seasonal peaks throughout the calendar year."),
            ("Centroids Download:", "Export cluster centroids as a CSV spreadsheet for academic appendices.")
        ]
    )

    # ==========================================
    # SLIDE 12: Promotional Planning & HTML Reporting
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "11. Planning Recommendations & Executive Report")

    add_card(slide12, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Evidence-Based Promotional Hypotheses",
        [
            ("Strategic Campaign Cards:", "Identifies optimal marketing launch windows 4–6 weeks prior to peak search surges."),
            ("Campaign Example 1:", "'Pre-Summer Mountain Escape & Eco-Tourism Drive' for Hill Station states (Launch late Q1/early Q2)."),
            ("Campaign Example 2:", "'Winter Sun & Coastal Heritage Awareness Drive' for Coastal states (Launch Q3/early Q4)."),
            ("Campaign Example 3:", "'Responsible Safari & Conservation Trail Drive' during open national park months."),
            ("Field Validation Metrics:", "Recommends tracking hotel inquiries, state tourism portal clicks, and flight bookings.")
        ]
    )

    add_card(slide12, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Executive Report & Data Exports",
        [
            ("1. CSV Recommendations Export:", "Download the complete actionable recommendations table for tourism department briefings."),
            ("2. Executive HTML Report:", "1-click generation of a self-contained, publication-ready project summary HTML report:"),
            ("Report Contents:", "Includes executive summary metrics, preprocessing audit log, cluster centroid tables, and planning hypotheses."),
            ("Zero Dependencies:", "Opens in any web browser without needing Python or specialized software.")
        ]
    )

    # ==========================================
    # SLIDE 13: Ethical Safeguards & Viva Summary
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "12. Ethical Safeguards & Viva Voce Summary")

    add_card(slide13, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0),
        "Mandatory Ethical & Interpretation Rules",
        [
            ("Curiosity != Physical Footfall:", "Google Trends measures digital information-seeking, NOT actual visitor counts, hotel bookings, or resident intelligence."),
            ("Digital Divide Bias:", "Regions with lower internet penetration reflect relative interest among active searchers, not total population."),
            ("Non-Stereotyping Principle:", "Never state 'Region X has poor tourism interest.' State 'Region X showed lower relative search index during the analyzed window.'"),
            ("Pre-Implementation Verification:", "Government departments must cross-reference suggestions with Ministry of Tourism ground data before allocating marketing budgets.")
        ]
    )

    add_card(slide13, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0),
        "Key Viva Takeaways for Examiners",
        [
            ("1. Real-World Relevance:", "Addresses actual seasonal demand matching for regional state tourism boards."),
            ("2. Technical Rigor:", "Implements internal standardization, 42 seasonal features, and multi-metric validation (Elbow, Silhouette, DBI)."),
            ("3. Distance Geometry:", "Directly contrasts Euclidean L2 (K-Means) with Manhattan L1 (K-Medians)."),
            ("4. Algorithmic Stability:", "Proves reproducibility across 10 random seeds using Adjusted Rand Index (ARI)."),
            ("5. Complete Interface:", "Professional 9-page Streamlit dashboard runnable locally in 1 click.")
        ]
    )

    prs.save(output_path)
    print(f"User manual presentation generated successfully at: {output_path}")
    return output_path


if __name__ == "__main__":
    build_presentation()

