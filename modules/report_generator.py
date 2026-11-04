"""
Report Generator Module for Tourism Planning Dashboard
======================================================
Compiles an executive summary report in HTML format with styled
cards, metric tables, cluster profiles, and planning suggestions.
"""

from datetime import datetime


def generate_html_summary_report(
    project_title,
    app_subtitle,
    summary_stats,
    preprocessing_report,
    clustering_metrics,
    df_profiles,
    df_recommendations,
    pca_variance,
    selected_algo,
    selected_k,
):
    """
    Generate an executive HTML project summary report for academic evaluation.
    """
    timestamp = datetime.now().strftime("%d %B %Y, %I:%M %p")

    # Format PCA variance
    if pca_variance is not None:
        try:
            if hasattr(pca_variance, "__iter__"):
                pca_var_str = f"{float(sum(pca_variance)):.1f}%"
            else:
                pca_var_str = f"{float(pca_variance):.1f}%"
        except Exception:
            pca_var_str = "N/A"
    else:
        pca_var_str = "N/A"

    # Format Silhouette
    sil_val = clustering_metrics.get('Silhouette_Score', clustering_metrics.get('silhouette', 'N/A'))
    if isinstance(sil_val, (int, float)):
        sil_str = f"{sil_val:.4f}"
    else:
        sil_str = str(sil_val)

    # Generate Profile Table HTML
    profile_html = df_profiles.to_html(classes="table", border=0) if df_profiles is not None and not df_profiles.empty else "<p>No profile data available.</p>"

    # Generate Recommendations HTML
    rec_html = ""
    if df_recommendations is not None and not df_recommendations.empty:
        for _, r in df_recommendations.iterrows():
            rec_html += f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #2563eb; padding: 14px; margin-bottom: 12px; border-radius: 6px;">
                <div style="font-weight: 700; color: #1e3a8a; font-size: 15px;">{r.get('Cluster_ID', 'Cluster')} — {r.get('Campaign_Strategy', 'Strategy')}</div>
                <div style="font-size: 12px; color: #475569; margin: 4px 0;"><strong>Topic:</strong> {r.get('Target_Topic', 'N/A')} | <strong>Timing:</strong> {r.get('Peak_Quarter', 'N/A')}</div>
                <div style="font-size: 13px; color: #1e293b; margin: 6px 0;"><strong>Rationale:</strong> {r.get('Strategic_Rationale', '')}</div>
                <div style="font-size: 12px; color: #059669;"><strong>Validation Metrics:</strong> {r.get('Validation_Metrics', '')}</div>
            </div>
            """
    else:
        rec_html = "<p>No recommendations generated.</p>"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{project_title} — Executive Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #0f172a; max-width: 900px; margin: 30px auto; padding: 0 20px; }}
        h1 {{ color: #1e293b; font-size: 24px; border-bottom: 2px solid #2563eb; padding-bottom: 8px; margin-bottom: 4px; }}
        h2 {{ color: #1e3a8a; font-size: 18px; margin-top: 24px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; }}
        .header-meta {{ font-size: 12px; color: #64748b; margin-bottom: 20px; }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 16px 0; }}
        .stat-card {{ background: #f1f5f9; padding: 12px; border-radius: 6px; text-align: center; border: 1px solid #e2e8f0; }}
        .stat-val {{ font-size: 20px; font-weight: bold; color: #1e40af; }}
        .stat-lbl {{ font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 600; }}
        .alert {{ background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #3b82f6; padding: 12px; font-size: 13px; border-radius: 4px; margin: 16px 0; }}
        .table {{ width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13px; }}
        .table th, .table td {{ padding: 8px 12px; border: 1px solid #e2e8f0; text-align: left; }}
        .table th {{ background: #f8fafc; font-weight: 600; color: #334155; }}
        .footer {{ font-size: 11px; color: #94a3b8; text-align: center; margin-top: 40px; border-top: 1px solid #e2e8f0; padding-top: 14px; }}
    </style>
</head>
<body>
    <h1>{project_title}</h1>
    <div style="font-weight: 600; color: #0284c7; font-size: 14px;">{app_subtitle}</div>
    <div class="header-meta">Generated on: {timestamp} | Academic Course: CSE396 Unsupervised Learning Project</div>

    <div class="alert">
        <strong>Important Decision-Support Safeguard:</strong> This report is intended as a planning aid for state and union territory tourism departments. Google Trends search interest represents relative online curiosity, not actual tourist footfalls or bookings. Hypotheses must be validated against physical ground metrics.
    </div>

    <h2>1. Executive Summary & Core Parameters</h2>
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-val">{summary_stats.get('total_regions', 0)}</div>
            <div class="stat-lbl">Analyzed Regions</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">{summary_stats.get('total_topics', 6)}</div>
            <div class="stat-lbl">Tourism Topics</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">{selected_algo} (K={selected_k})</div>
            <div class="stat-lbl">Model Configuration</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">{sil_str}</div>
            <div class="stat-lbl">Silhouette Score</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">{pca_var_str}</div>
            <div class="stat-lbl">PCA Retained Variance</div>
        </div>
    </div>

    <h2>2. Preprocessing & Data Validation Summary</h2>
    <ul>
        <li><strong>Original Records Parsed:</strong> {preprocessing_report.get('original_records', 0)}</li>
        <li><strong>Duplicates Removed:</strong> {preprocessing_report.get('duplicates_removed', 0)}</li>
        <li><strong>Short Gaps Interpolated (<=2 weeks):</strong> {preprocessing_report.get('short_gaps_interpolated', 0)}</li>
        <li><strong>Zeros Preserved (Low Volume):</strong> {preprocessing_report.get('zeros_preserved', 0)}</li>
        <li><strong>Eligible Regions Retained:</strong> {len(preprocessing_report.get('eligible_regions', []))}</li>
    </ul>

    <h2>3. Regional Cluster Profiles & Topic Averages</h2>
    {profile_html}

    <h2>4. Targeted Promotional Planning Hypotheses</h2>
    {rec_html}

    <h2>5. Academic Limitations</h2>
    <ol style="font-size: 13px; color: #334155;">
        <li><strong>Relative Normalization:</strong> Google Trends values are indexed 0–100 relative to the highest region/time query share, not absolute search counts.</li>
        <li><strong>Curiosity vs. Reality:</strong> Online search curiosity may reflect casual interest, media events, or holiday dreaming rather than actual completed journeys.</li>
        <li><strong>Sampling Variation:</strong> Smaller Union Territories have smaller query pools in Google's sample.</li>
        <li><strong>PCA Approximation:</strong> 2D PCA visual representation omits a small fraction of higher-dimensional variance.</li>
    </ol>

    <div class="footer">
        Regional Tourism Promotion Planner • CSE396 Unsupervised Learning Project • Built with Streamlit, Scikit-learn, and Plotly
    </div>
</body>
</html>
"""
    return html_content

