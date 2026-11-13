"""
Generate an executive, visually attractive 10-slide PowerPoint presentation
integrating charts, destination photography, and cultural visuals.
"""

from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen format
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Brand Palette
    C_PRIMARY_DARK = RGBColor(18, 56, 42)      # Deep Forest Green (#12382A)
    C_PRIMARY_MID  = RGBColor(28, 76, 56)      # Mid Forest (#1C4C38)
    C_PRIMARY_TINT = RGBColor(240, 246, 242)   # Pale Green Tint
    C_ACCENT_GOLD  = RGBColor(196, 154, 42)    # Warm Kerala Gold (#C49A2A)
    C_EMERALD      = RGBColor(43, 138, 98)     # Accent Emerald (#2B8A62)
    C_BG_LIGHT     = RGBColor(247, 249, 247)   # Crisp Light Sage Tint (#F7F9F7)
    C_CARD_BG      = RGBColor(255, 255, 255)   # Pure White Card
    C_CARD_BORDER  = RGBColor(220, 228, 222)   # Subtle Border
    C_TEXT_DARK    = RGBColor(24, 34, 28)      # Charcoal Dark Ink
    C_TEXT_MUTED   = RGBColor(88, 102, 94)     # Slate Green Muted
    C_WHITE        = RGBColor(255, 255, 255)
    C_BADGE_ROSE   = RGBColor(185, 45, 55)

    assets_dir = Path("11_Presentation/assets")

    def set_slide_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, kicker: str, title: str, subtitle: str = ""):
        # Kicker badge / tag
        k_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
        tf_k = k_box.text_frame
        tf_k.word_wrap = True
        tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        p_k = tf_k.paragraphs[0]
        p_k.text = kicker.upper()
        p_k.font.size = Pt(9.5)
        p_k.font.bold = True
        p_k.font.color.rgb = C_ACCENT_GOLD
        p_k.font.name = "Arial"

        # Main Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.55))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = C_PRIMARY_DARK
        p_t.font.name = "Georgia"

        # Subtitle
        if subtitle:
            s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.32))
            tf_s = s_box.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            p_s.text = subtitle
            p_s.font.size = Pt(10.5)
            p_s.font.color.rgb = C_TEXT_MUTED
            p_s.font.name = "Arial"

        # Subtle divider rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.62), Inches(11.733), Inches(0.015))
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_CARD_BORDER
        rule.line.fill.background()

    def create_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Cover with Hero Image)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, C_PRIMARY_DARK)

    # Accent Vertical Gold Line
    dec1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(0.1), Inches(5.9))
    dec1.fill.solid()
    dec1.fill.fore_color.rgb = C_ACCENT_GOLD
    dec1.line.fill.background()

    # Left Column: Titles & Details
    k1 = s1.shapes.add_textbox(Inches(1.15), Inches(1.0), Inches(6.8), Inches(0.35))
    p1_k = k1.text_frame.paragraphs[0]
    p1_k.text = "DATA-DRIVEN TOURISM INTELLIGENCE PLATFORM"
    p1_k.font.size = Pt(10.5)
    p1_k.font.bold = True
    p1_k.font.color.rgb = C_ACCENT_GOLD

    t1 = s1.shapes.add_textbox(Inches(1.15), Inches(1.4), Inches(6.8), Inches(1.7))
    tf1_t = t1.text_frame
    tf1_t.word_wrap = True
    p1_t = tf1_t.paragraphs[0]
    p1_t.text = "Kerala Tourism\nIntelligence"
    p1_t.font.size = Pt(36)
    p1_t.font.bold = True
    p1_t.font.color.rgb = C_WHITE
    p1_t.font.name = "Georgia"

    p1_t2 = tf1_t.add_paragraph()
    p1_t2.text = "Unlocking High-Yield Hospitality & Investment Opportunities"
    p1_t2.font.size = Pt(16)
    p1_t2.font.color.rgb = RGBColor(215, 230, 222)
    p1_t2.font.name = "Arial"

    d1 = s1.shapes.add_textbox(Inches(1.15), Inches(3.25), Inches(6.6), Inches(1.1))
    tf1_d = d1.text_frame
    tf1_d.word_wrap = True
    p1_d = tf1_d.paragraphs[0]
    p1_d.text = (
        "An end-to-end data analytics and machine learning platform analyzing 25 major destinations across Kerala. "
        "Synthesizing 2022–2024 footfall growth, Google Trends India demand (2021–2026), unsupervised K-Means "
        "segmentation, infrastructure deficit scoring, and 5-year venture ROI forecasting."
    )
    p1_d.font.size = Pt(11)
    p1_d.font.color.rgb = RGBColor(185, 202, 192)

    # 4 Metric Cards in 2x2 grid
    metric_cards = [
        ("25", "Destinations Audited", "All 14 Districts Covered"),
        ("3 Clusters", "Machine Learning Segments", "Standard & Robust Scaling"),
        ("29,585", "Cleaned Search Points", "Google Trends India (2021-2026)"),
        ("14 Corridors", "High Gap Opportunities", "Surging Footfall & Supply Deficits"),
    ]
    for idx, (m_val, m_lbl, m_sub) in enumerate(metric_cards):
        row = idx // 2
        col = idx % 2
        cx = Inches(1.15 + col * 3.35)
        cy = Inches(4.55 + row * 1.05)
        cw = Inches(3.2)
        ch = Inches(0.95)
        create_card(s1, cx, cy, cw, ch, bg_color=C_PRIMARY_MID, border_color=RGBColor(45, 105, 80))

        tb = s1.shapes.add_textbox(cx + Inches(0.12), cy + Inches(0.08), cw - Inches(0.24), ch - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = m_val
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_ACCENT_GOLD
        p.font.name = "Georgia"

        p2 = tf.add_paragraph()
        p2.text = f"{m_lbl} • {m_sub}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = RGBColor(220, 235, 225)

    # Right Hero Image with Gold Frame
    hero_img = assets_dir / "cover_hero.jpg"
    if hero_img.exists():
        # Outer Gold Border Box
        gold_frame = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.15), Inches(0.8), Inches(4.35), Inches(5.9))
        gold_frame.fill.solid()
        gold_frame.fill.fore_color.rgb = C_PRIMARY_MID
        gold_frame.line.color.rgb = C_ACCENT_GOLD
        gold_frame.line.width = Pt(1.5)

        s1.shapes.add_picture(str(hero_img), Inches(8.25), Inches(0.9), Inches(4.15), Inches(5.7))

    # =========================================================================
    # SLIDE 2: STRATEGIC CONTEXT & THE TOURISM PARADOX
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, C_BG_LIGHT)
    add_header(s2, "Strategic Context & Problem Statement", "Resolving the Kerala Tourism Investment Paradox",
               "Balancing overtourism in legacy hubs with uncapitalized surge in emerging eco-corridors.")

    # Card 1: Saturated Classic Hubs (with Kochi photo)
    cw2 = Inches(3.78)
    ch2 = Inches(5.4)
    create_card(s2, Inches(0.8), Inches(1.85), cw2, ch2)
    kochi_img = assets_dir / "card_kochi.jpg"
    if kochi_img.exists():
        s2.shapes.add_picture(str(kochi_img), Inches(0.95), Inches(2.0), Inches(3.48), Inches(1.75))

    tb2_1 = s2.shapes.add_textbox(Inches(0.95), Inches(3.85), Inches(3.48), Inches(3.2))
    tf2_1 = tb2_1.text_frame
    tf2_1.word_wrap = True
    p = tf2_1.paragraphs[0]
    p.text = "1. SATURATED CLASSIC HUBS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY_DARK
    p.font.name = "Georgia"

    bullets_1 = [
        "Legacy nodes (Fort Kochi, Kovalam) face severe land price inflation, margin compression, and seasonal crowding.",
        "High baseline accommodation supply creates intense price wars for independent homestays and hotels.",
        "Uninformed entrepreneurs over-invest in crowded nodes due to lack of granular regional intelligence."
    ]
    for b in bullets_1:
        p = tf2_1.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(4)

    # Card 2: Emerging Eco-Corridors (with Vagamon photo)
    create_card(s2, Inches(4.78), Inches(1.85), cw2, ch2)
    vaga_img = assets_dir / "card_vagamon.jpg"
    if vaga_img.exists():
        s2.shapes.add_picture(str(vaga_img), Inches(4.93), Inches(2.0), Inches(3.48), Inches(1.75))

    tb2_2 = s2.shapes.add_textbox(Inches(4.93), Inches(3.85), Inches(3.48), Inches(3.2))
    tf2_2 = tb2_2.text_frame
    tf2_2.word_wrap = True
    p = tf2_2.paragraphs[0]
    p.text = "2. EMERGING ECO-CORRIDORS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY_DARK
    p.font.name = "Georgia"

    bullets_2 = [
        "Rising nature and adventure corridors (Vagamon, Kumarakom, Bekal) exhibit footfall growth up to +109%.",
        "Critical deficits in quality dining, experiential stays, and branded homestays constrain tourist spend.",
        "Lack of structured feasibility metrics prevents institutional debt and capital from entering rural zones."
    ]
    for b in bullets_2:
        p = tf2_2.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(4)

    # Card 3: Platform Solution & Resolution
    create_card(s2, Inches(8.76), Inches(1.85), cw2, ch2, bg_color=C_PRIMARY_TINT, border_color=C_EMERALD)
    tb2_3 = s2.shapes.add_textbox(Inches(8.95), Inches(2.0), Inches(3.4), Inches(5.1))
    tf2_3 = tb2_3.text_frame
    tf2_3.word_wrap = True

    p = tf2_3.paragraphs[0]
    p.text = "THE SOLUTION"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p2 = tf2_3.add_paragraph()
    p2.text = "Data Science Decision Engine"
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = C_PRIMARY_DARK
    p2.font.name = "Georgia"
    p2.space_after = Pt(10)

    bullets_3 = [
        "Integrates multi-source data: official footfall records, Google Maps POIs, transport hubs, and 5-year Google Trends.",
        "Evaluates cluster-relative supply deficits (Overall Gap Score) rather than generic statewide averages.",
        "Maps 25 destinations onto an actionable 2×2 Opportunity Matrix (Growth vs. Gap).",
        "Provides dynamic 5-year cash flow and ROI simulator to derisk hospitality investments."
    ]
    for b in bullets_3:
        p = tf2_3.add_paragraph()
        p.text = f"✔ {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: DATA ARCHITECTURE & METHODOLOGY
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, C_BG_LIGHT)
    add_header(s3, "Architecture & Pipeline", "Full-Stack Data Science & Engineering Pipeline",
               "Modular Python data pipeline with production-grade separation of concerns and Flask dashboard.")

    s3_steps = [
        ("Phase 01", "Data Acquisition & Audit", [
            "Official Kerala Tourism annual statistics (2022–2024 calendar visits).",
            "Scraped Google Maps POIs: Hotels, Resorts, Homestays, Restaurants, Attractions.",
            "Accessibility metrics: distance to nearest airports & primary/alternative railway terminals."
        ]),
        ("Phase 02", "Cleaning & Imputation", [
            "Zero-supply handling: replaced unrecorded counts with median SimpleImputer for ML.",
            "Isolated 5 duplicate-key search terms (610 records) to clean Google Trends dataset.",
            "Audited data quality notes: 16 destinations flagged with estimates; 9 official."
        ]),
        ("Phase 03", "Machine Learning & Scoring", [
            "Benchmarked StandardScaler vs RobustScaler vs PCA(2) for K-Means (k=3).",
            "Calculated cluster-relative supply deficits (Overall Gap Score).",
            "Mapped 25 destinations into 2×2 Growth vs. Infrastructure Gap quadrants."
        ]),
        ("Phase 04", "Frontend & Interactive API", [
            "Modern Flask web application with Jinja2 modular templates.",
            "REST JSON endpoints for real-time trend querying & financial calculations.",
            "Chart.js interactive visualizations for demand cycles and cash-flow curves."
        ])
    ]

    for idx, (p_tag, p_title, p_bullets) in enumerate(s3_steps):
        cx = Inches(0.8 + idx * 2.98)
        cy = Inches(1.85)
        cw = Inches(2.8)
        ch = Inches(3.6)
        create_card(s3, cx, cy, cw, ch)

        tb = s3.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.2), cw - Inches(0.4), ch - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_tag_p = tf.paragraphs[0]
        p_tag_p.text = p_tag.upper()
        p_tag_p.font.size = Pt(9.5)
        p_tag_p.font.bold = True
        p_tag_p.font.color.rgb = C_ACCENT_GOLD

        p_t = tf.add_paragraph()
        p_t.text = p_title
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = C_PRIMARY_DARK
        p_t.font.name = "Georgia"
        p_t.space_after = Pt(8)

        for b in p_bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(8.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(4)

    # Bottom Architecture Summary Banner
    create_card(s3, Inches(0.8), Inches(5.65), Inches(11.733), Inches(1.4), bg_color=C_PRIMARY_DARK, border_color=C_ACCENT_GOLD)
    pipe_img = assets_dir / "pipeline_banner.jpg"
    if pipe_img.exists():
        s3.shapes.add_picture(str(pipe_img), Inches(0.95), Inches(5.75), Inches(2.35), Inches(1.2))

    tb3_b = s3.shapes.add_textbox(Inches(3.45), Inches(5.72), Inches(8.85), Inches(1.25))
    tf3_b = tb3_b.text_frame
    tf3_b.word_wrap = True

    p = tf3_b.paragraphs[0]
    p.text = "MODULAR DESIGN & 100% REPRODUCIBILITY"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT_GOLD

    p2 = tf3_b.add_paragraph()
    p2.text = (
        "• Production Pipeline: All stages in 05_Source_Code execute end-to-end via python run_pipeline.py with dry-run & persistent --save flags.\n"
        "• Technology Stack: Python 3.11, Pandas, Scikit-Learn, Plotly, Flask, Jinja2, Chart.js — fully decoupled, zero vendor lock-in.\n"
        "• Governance & Safety: Data quality flags guarantee that official statistics and provisional projections are never conflated."
    )
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = RGBColor(220, 235, 225)

    # =========================================================================
    # SLIDE 4: VISITOR GROWTH DYNAMICS & DATA TRANSPARENCY
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, C_BG_LIGHT)
    add_header(s4, "Visitor Footfall Dynamics", "Visitor Growth Surge & Data Transparency (2022–2024)",
               "Accelerated recovery across leisure destinations paired with rigorous estimation audit.")

    # Left: High-Res Growth Bar Chart
    cw4_l = Inches(6.8)
    ch4_main = Inches(5.4)
    create_card(s4, Inches(0.8), Inches(1.85), cw4_l, ch4_main)
    chart_growth = assets_dir / "chart_visitor_growth.png"
    if chart_growth.exists():
        s4.shapes.add_picture(str(chart_growth), Inches(0.95), Inches(2.0), Inches(6.5), Inches(5.1))

    # Right: Munnar Top Growth Photo Card
    cw4_r = Inches(4.733)
    create_card(s4, Inches(7.8), Inches(1.85), cw4_r, Inches(2.6))
    munnar_img = assets_dir / "growth_munnar.jpg"
    if munnar_img.exists():
        s4.shapes.add_picture(str(munnar_img), Inches(7.95), Inches(1.95), Inches(4.433), Inches(2.0))

    tb4_m = s4.shapes.add_textbox(Inches(7.95), Inches(4.0), Inches(4.433), Inches(0.4))
    p = tb4_m.text_frame.paragraphs[0]
    p.text = "MUNNAR LEADS SURGE: +109.2% (1.08M → 2.26M Visits)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY_DARK

    # Right Bottom: Data Transparency Audit Card
    create_card(s4, Inches(7.8), Inches(4.6), cw4_r, Inches(2.65))
    tb4_audit = s4.shapes.add_textbox(Inches(8.0), Inches(4.7), Inches(4.333), Inches(2.4))
    tf4_audit = tb4_audit.text_frame
    tf4_audit.word_wrap = True

    p = tf4_audit.paragraphs[0]
    p.text = "DATA TRANSPARENCY AUDIT"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT_GOLD

    p2 = tf4_audit.add_paragraph()
    p2.text = "16 of 25 Destinations Contain Estimates"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = C_PRIMARY_DARK
    p2.font.name = "Georgia"

    p3 = tf4_audit.add_paragraph()
    p3.text = (
        "• Official data published by Kerala Tourism contains derived or provisional estimates for emerging rural sites.\n"
        "• 9 Destinations (e.g. Munnar, Kumarakom, Kochi) are strictly official with no estimation notes.\n"
        "• 16 Destinations are explicitly flagged as 'Contains estimates' in our pipeline, protecting investors from spurious correlations."
    )
    p3.font.size = Pt(8.5)
    p3.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 5: UNSUPERVISED MACHINE LEARNING SEGMENTATION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, C_BG_LIGHT)
    add_header(s5, "Clustering & Machine Learning", "Destination Segmentation via K-Means Clustering",
               "Evaluating 8 structural features across StandardScaler, RobustScaler, and 2D PCA projection.")

    # Left: Model Benchmark Chart
    cw5_l = Inches(5.8)
    create_card(s5, Inches(0.8), Inches(1.85), cw5_l, Inches(5.4))
    chart_model = assets_dir / "chart_model_benchmark.png"
    if chart_model.exists():
        s5.shapes.add_picture(str(chart_model), Inches(0.95), Inches(2.0), Inches(5.5), Inches(5.05))

    # Right: 3 Cluster Profile Cards with Representative Images
    clusters_info = [
        ("cluster_urban.jpg", "Cluster 0: Urban Hubs (3 Destinations)", "Kochi City, Kozhikode, Thiruvananthapuram",
         "Avg Hotels: 346.0 | Avg Restaurants: 912.7 | 22.3 km to Airport. Dense corporate & transit gateways."),
        ("cluster_nature.jpg", "Cluster 1: Developing & Nature (14 Destinations)", "Vagamon, Silent Valley, Ponmudi, Bekal, etc.",
         "Avg Hotels: 39.2 | Avg Homestays: 88.0 | 70.7 km to Airport. Rural eco-travel, severe dining deficits."),
        ("cluster_resort.jpg", "Cluster 2: Established Leisure (8 Destinations)", "Munnar, Kumarakom, Varkala, Thekkady, etc.",
         "Avg Resorts: 164.3 | Avg Homestays: 401.3 | Resort Rating: 4.44/5. High brand equity & leisure spend.")
    ]

    for idx, (img_name, c_title, c_dests, c_desc) in enumerate(clusters_info):
        cy = Inches(1.85 + idx * 1.83)
        cw = Inches(5.733)
        ch = Inches(1.72)
        create_card(s5, Inches(6.8), cy, cw, ch)

        img_p = assets_dir / img_name
        if img_p.exists():
            s5.shapes.add_picture(str(img_p), Inches(6.95), cy + Inches(0.12), Inches(1.65), Inches(1.48))

        tb = s5.shapes.add_textbox(Inches(8.7), cy + Inches(0.1), Inches(3.7), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = c_title
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_PRIMARY_DARK
        p1.font.name = "Georgia"

        p2 = tf.add_paragraph()
        p2.text = c_dests
        p2.font.size = Pt(8.5)
        p2.font.italic = True
        p2.font.color.rgb = C_EMERALD

        p3 = tf.add_paragraph()
        p3.text = c_desc
        p3.font.size = Pt(8)
        p3.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 6: DIGITAL SEARCH SIGNALS (GOOGLE TRENDS)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, C_BG_LIGHT)
    add_header(s6, "Digital Consumer Demand", "Decoding Traveler Intent via Google Trends India (2021–2026)",
               "Standardized multi-pillar time series across 29,585 cleaned monthly observation points.")

    # Left: 4 Demand Pillar Cards in a 2x2 Grid
    pillars = [
        ("Pillar 01", "Destination Interest", "Munnar, Wayanad & Kochi lead gross Indian travel queries. Macro awareness peaks during winter holidays."),
        ("Pillar 02", "Accommodation Queries", "Surging demand for 'cliffside stays', 'private pool villas', and 'luxury houseboats'. Premium willingness to pay."),
        ("Pillar 03", "Tourism Activities", "Accelerating query growth for trekking, bamboo rafting, tea trails, and kayaking over passive sightseeing."),
        ("Pillar 04", "Food & Dining Intent", "Hyper-local search demand for Malabar Biryani, Thalassery snacks, and Toddy Shop duck roast outpaces generic dining.")
    ]

    for idx, (p_tag, p_name, p_desc) in enumerate(pillars):
        row = idx // 2
        col = idx % 2
        cx = Inches(0.8 + col * 3.35)
        cy = Inches(1.85 + row * 2.7)
        cw = Inches(3.2)
        ch = Inches(2.55)
        create_card(s6, cx, cy, cw, ch)

        tb = s6.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.2), cw - Inches(0.4), ch - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = p_tag.upper()
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = C_ACCENT_GOLD

        p2 = tf.add_paragraph()
        p2.text = p_name
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_PRIMARY_DARK
        p2.font.name = "Georgia"
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = p_desc
        p3.font.size = Pt(9)
        p3.font.color.rgb = C_TEXT_DARK

    # Right: 2 Thematic Photos (Varkala Stays + Malabar Food)
    cw6_r = Inches(5.733)
    # Photo 1: Varkala
    create_card(s6, Inches(7.8), Inches(1.85), cw6_r, Inches(2.55))
    varkala_img = assets_dir / "trends_varkala.jpg"
    if varkala_img.exists():
        s6.shapes.add_picture(str(varkala_img), Inches(7.95), Inches(1.95), Inches(2.5), Inches(2.35))
    tb_v = s6.shapes.add_textbox(Inches(10.6), Inches(2.0), Inches(2.8), Inches(2.2))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True
    p = tf_v.paragraphs[0]
    p.text = "ACCOMMODATION SURGE"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p2 = tf_v.add_paragraph()
    p2.text = "Varkala Cliffside Stays"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = C_PRIMARY_DARK
    p3 = tf_v.add_paragraph()
    p3.text = "Search interest for cliff villas has grown 4x faster than traditional beach resorts since 2022."
    p3.font.size = Pt(8.5)
    p3.font.color.rgb = C_TEXT_MUTED

    # Photo 2: Food
    create_card(s6, Inches(7.8), Inches(4.55), cw6_r, Inches(2.55))
    food_img = assets_dir / "trends_food.jpg"
    if food_img.exists():
        s6.shapes.add_picture(str(food_img), Inches(7.95), Inches(4.65), Inches(2.5), Inches(2.35))
    tb_f = s6.shapes.add_textbox(Inches(10.6), Inches(4.7), Inches(2.8), Inches(2.2))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "CULINARY TOURISM"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT_GOLD
    p2 = tf_f.add_paragraph()
    p2.text = "Regional Food Identity"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = C_PRIMARY_DARK
    p3 = tf_f.add_paragraph()
    p3.text = "Queries for Malabar snacks and seafood cuisine reveal massive uncapitalized culinary market opportunities."
    p3.font.size = Pt(8.5)
    p3.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: INFRASTRUCTURE DEFICIT & OPPORTUNITY MATRIX
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, C_BG_LIGHT)
    add_header(s7, "Business Opportunity Evaluation", "Infrastructure Deficit Scoring & 2×2 Opportunity Matrix",
               "Evaluating cluster-relative supply gaps against footfall momentum to classify 25 destinations.")

    # Left: Opportunity Scatter Plot Chart
    cw7_l = Inches(6.4)
    create_card(s7, Inches(0.8), Inches(1.85), cw7_l, Inches(5.4))
    chart_quad = assets_dir / "chart_opportunity_quadrants.png"
    if chart_quad.exists():
        s7.shapes.add_picture(str(chart_quad), Inches(0.95), Inches(1.95), Inches(6.1), Inches(5.2))

    # Right: 4 Quadrant Strategic Cards
    quad_cards = [
        ("High Gap + Positive Growth (14 Dests)", C_EMERALD, RGBColor(240, 248, 243),
         "Primary Greenfield Targets: Kumarakom (Gap +94.1), Vagamon (Gap +67.4), Thekkady (Gap +54.9). Aggressive rollout of eco-resorts & dining."),
        ("Low Gap + Positive Growth (8 Dests)", RGBColor(43, 108, 176), RGBColor(243, 246, 250),
         "Quality / Niche Upgrades: Munnar (+109.2% growth, Gap -42.1), Varkala (+62.9%). Focus on experiential dining and premium service differentiation."),
        ("High Gap + Negative Growth (1 Dest)", C_BADGE_ROSE, RGBColor(254, 246, 246),
         "Cautionary Turnaround: Meenkunnu–Payyambalam (Kannur coast: -11.5% growth). Requires public infrastructure stimulus before private capital scale."),
        ("Low Gap + Negative Growth (2 Dests)", RGBColor(113, 128, 150), RGBColor(250, 250, 250),
         "Consolidation & Asset Yield: Konni, Palaruvi. Saturated relative to footfall; focus strictly on optimizing existing yields.")
    ]

    for idx, (q_title, q_col, q_bg, q_desc) in enumerate(quad_cards):
        cy = Inches(1.85 + idx * 1.37)
        cw = Inches(5.133)
        ch = Inches(1.25)
        create_card(s7, Inches(7.4), cy, cw, ch, bg_color=q_bg, border_color=q_col)

        tb = s7.shapes.add_textbox(Inches(7.55), cy + Inches(0.1), cw - Inches(0.3), ch - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = q_title.upper()
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = q_col

        p2 = tf.add_paragraph()
        p2.text = q_desc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 8: TAILORED INVESTMENT BLUEPRINTS (REGIONAL SPOTLIGHTS)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, C_BG_LIGHT)
    add_header(s8, "Venture Blueprints", "High-Conviction Investment Blueprints by Regional Corridor",
               "Detailed case studies translating data intelligence into commercial hospitality concepts.")

    blueprints = [
        ("blueprint_kumarakom.jpg", "Kumarakom", "Backwater Luxury", "Gap: +94.1 | Footfall: +65.8%",
         "Waterfront Dining & Eco-Villas",
         "High deficit in dining & luxury villas. Surging footfall (+65.8%) creates ripe demand for independent experiential dining outside resorts."),
        ("blueprint_vagamon.jpg", "Vagamon", "Eco-Adventure", "Gap: +67.4 | Footfall: +35.2%",
         "Glamping & Activity Lodges",
         "High search demand for trekking & paragliding contrasts with severe homestay shortage. Ideal for off-grid eco-stays and adventure cafes."),
        ("blueprint_munnar.jpg", "Munnar", "Quality Upgrade", "Footfall: +109.2% | Rating: 3.9/5",
         "Farm-to-Table Dining & Cafes",
         "Massive footfall surge (2.26M visits) but restaurants lag at 3.9/5 average rating. High pricing power for artisanal culinary experiences."),
        ("blueprint_bekal.jpg", "North Malabar", "Heritage Circuit", "Bekal Gap: +147.5 | Kannur Airport",
         "Heritage Homestay Circuit",
         "Driven by Kannur airport connectivity and Theyyam festivals. Severe homestay deficit (>150 units below state mean) offers network opportunity.")
    ]

    for idx, (img_name, dest, kicker, stats, concept, rationale) in enumerate(blueprints):
        cx = Inches(0.8 + idx * 2.98)
        cy = Inches(1.85)
        cw = Inches(2.8)
        ch = Inches(5.4)
        create_card(s8, cx, cy, cw, ch)

        img_p = assets_dir / img_name
        if img_p.exists():
            s8.shapes.add_picture(str(img_p), cx + Inches(0.12), cy + Inches(0.12), Inches(2.56), Inches(1.6))

        tb = s8.shapes.add_textbox(cx + Inches(0.15), cy + Inches(1.8), cw - Inches(0.3), Inches(3.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = kicker.upper()
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = C_ACCENT_GOLD

        p2 = tf.add_paragraph()
        p2.text = dest
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = C_PRIMARY_DARK
        p2.font.name = "Georgia"

        p3 = tf.add_paragraph()
        p3.text = stats
        p3.font.size = Pt(8)
        p3.font.bold = True
        p3.font.color.rgb = C_EMERALD
        p3.space_after = Pt(6)

        p4 = tf.add_paragraph()
        p4.text = f"Concept: {concept}"
        p4.font.size = Pt(9.5)
        p4.font.bold = True
        p4.font.color.rgb = C_PRIMARY_MID
        p4.space_after = Pt(6)

        p5 = tf.add_paragraph()
        p5.text = rationale
        p5.font.size = Pt(8.5)
        p5.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 9: FINANCIAL SIMULATION & ROI ECONOMICS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, C_BG_LIGHT)
    add_header(s9, "Financial Simulation & Modeling", "Tourism Venture Feasibility & ROI Simulator",
               "Ground-truthed financial modeling across 4 standardized hospitality business archetypes.")

    # Left: Financial ROI Chart
    cw9_l = Inches(5.8)
    create_card(s9, Inches(0.8), Inches(1.85), cw9_l, Inches(5.4))
    chart_fin = assets_dir / "chart_financial_roi.png"
    if chart_fin.exists():
        s9.shapes.add_picture(str(chart_fin), Inches(0.95), Inches(1.95), Inches(5.5), Inches(5.2))

    # Right: Financial Table & Key Takeaway
    cw9_r = Inches(5.733)
    create_card(s9, Inches(6.8), Inches(1.85), cw9_r, Inches(2.9))

    tb9_t = s9.shapes.add_textbox(Inches(6.95), Inches(1.95), Inches(5.4), Inches(0.4))
    p = tb9_t.text_frame.paragraphs[0]
    p.text = "Hospitality Venture Archetypes & Economics"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY_DARK
    p.font.name = "Georgia"

    # Table
    t9_shape = s9.shapes.add_table(5, 5, Inches(6.95), Inches(2.4), Inches(5.4), Inches(2.2))
    t9 = t9_shape.table
    t9.columns[0].width = Inches(1.4)
    t9.columns[1].width = Inches(1.0)
    t9.columns[2].width = Inches(1.0)
    t9.columns[3].width = Inches(1.0)
    t9.columns[4].width = Inches(1.0)

    fin_rows = [
        ("Venture", "Capex", "Monthly", "ROI %", "Payback"),
        ("Homestay", "₹25.0 L", "₹85,000", "40.8%", "2.5 Yrs"),
        ("Restaurant", "₹35.0 L", "₹1,10,000", "37.7%", "2.7 Yrs"),
        ("Resort", "₹1.00 Cr", "₹2,30,000", "27.6%", "3.6 Yrs"),
        ("Hotel", "₹75.0 L", "₹1,70,000", "27.2%", "3.7 Yrs"),
    ]

    for r_i, r in enumerate(fin_rows):
        for c_i, val in enumerate(r):
            c = t9.cell(r_i, c_i)
            c.text = val
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.name = "Arial"
            if r_i == 0:
                c.fill.solid()
                c.fill.fore_color.rgb = C_PRIMARY_DARK
                p.font.bold = True
                p.font.color.rgb = C_WHITE
            else:
                p.font.color.rgb = C_TEXT_DARK
                if c_i == 3:
                    p.font.bold = True
                    p.font.color.rgb = C_EMERALD

    # Right Bottom: Capital Recovery Takeaways
    create_card(s9, Inches(6.8), Inches(4.9), cw9_r, Inches(2.35), bg_color=C_PRIMARY_TINT, border_color=C_EMERALD)
    tb9_rec = s9.shapes.add_textbox(Inches(7.0), Inches(5.0), Inches(5.3), Inches(2.1))
    tf9_rec = tb9_rec.text_frame
    tf9_rec.word_wrap = True

    p = tf9_rec.paragraphs[0]
    p.text = "STRATEGIC FINANCIAL TAKEAWAYS"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    bullets_f = [
        "Homestays deliver the quickest capital recovery (2.5 years) with minimal regulatory overhead.",
        "Experiential Dining captures immediate day-tripper cash flows without requiring heavy room capex.",
        "5-Year Cash Flow simulator built into platform provides institutional stress-testing for bank loans."
    ]
    for b in bullets_f:
        p = tf9_rec.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 10: STRATEGIC ROADMAP & CALL TO ACTION (Dark Closing)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, C_PRIMARY_DARK)

    # Left: Cultural Visual (Theyyam) with Gold Frame
    theyyam_img = assets_dir / "closing_theyyam.jpg"
    if theyyam_img.exists():
        gold_frame = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(4.15), Inches(5.9))
        gold_frame.fill.solid()
        gold_frame.fill.fore_color.rgb = C_PRIMARY_MID
        gold_frame.line.color.rgb = C_ACCENT_GOLD
        gold_frame.line.width = Pt(1.5)

        s10.shapes.add_picture(str(theyyam_img), Inches(0.9), Inches(0.9), Inches(3.95), Inches(5.7))

    # Right: Strategic Impact & Next Steps
    k10 = s10.shapes.add_textbox(Inches(5.2), Inches(0.85), Inches(7.3), Inches(0.35))
    p10_k = k10.text_frame.paragraphs[0]
    p10_k.text = "STRATEGIC IMPACT & NEXT STEPS"
    p10_k.font.size = Pt(10)
    p10_k.font.bold = True
    p10_k.font.color.rgb = C_ACCENT_GOLD

    t10 = s10.shapes.add_textbox(Inches(5.2), Inches(1.15), Inches(7.3), Inches(0.8))
    p10_t = t10.text_frame.paragraphs[0]
    p10_t.text = "Empowering Sustainable Tourism Growth in Kerala"
    p10_t.font.size = Pt(24)
    p10_t.font.bold = True
    p10_t.font.color.rgb = C_WHITE
    p10_t.font.name = "Georgia"

    s10_cards = [
        ("Immediate Value", [
            "De-risking private capital investments for local MSMEs and hospitality operators.",
            "Directing development toward underserved corridors to curb overtourism in saturated hubs.",
            "Providing evidence-based validation for bank loans and tourism state subsidy programs."
        ]),
        ("Technical Roadmap", [
            "Real-time OTA pricing API integration (MakeMyTrip, Booking.com, Airbnb).",
            "NLP sentiment extraction across thousands of Google & TripAdvisor traveler reviews.",
            "Predictive seasonality forecasting using Prophet & ARIMA machine learning models."
        ]),
        ("Call to Action", [
            "Engage Kerala Tourism Department for policy integration and real-time census data sharing.",
            "Establish sandbox pilots with regional entrepreneur networks in Kumarakom and Vagamon.",
            "Deploy white-label intelligence portals for district tourism promotion councils (DTPCs)."
        ])
    ]

    for idx, (col_title, col_bullets) in enumerate(s10_cards):
        cy = Inches(2.1 + idx * 1.55)
        cw = Inches(7.333)
        ch = Inches(1.42)
        card = create_card(s10, Inches(5.2), cy, cw, ch, bg_color=C_PRIMARY_MID, border_color=RGBColor(50, 110, 85))

        tb = s10.shapes.add_textbox(Inches(5.4), cy + Inches(0.12), cw - Inches(0.4), ch - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = col_title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_ACCENT_GOLD
        p1.font.name = "Georgia"

        for b in col_bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(8.5)
            p.font.color.rgb = RGBColor(230, 240, 235)

    # Save output
    output_path = Path("11_Presentation") / "Kerala_Tourism_Intelligence_Deck.pptx"
    prs.save(str(output_path))
    print(f"Presentation saved successfully to: {output_path.resolve()}")

if __name__ == "__main__":
    create_deck()
