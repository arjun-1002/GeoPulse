"""
Generate high-resolution branded charts for the Kerala Tourism Intelligence Presentation.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set visual style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#dce4de"
plt.rcParams["axes.linewidth"] = 0.8

ASSETS_DIR = Path("11_Presentation/assets")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. Visitor Growth Chart (Top Destinations)
# -------------------------------------------------------------
def make_growth_chart():
    df_growth = pd.read_csv("06_EDA_Analysis/visitor_growth_2022_2024.csv")
    df_top = df_growth.sort_values(by="Growth_2022_2024", ascending=True).tail(8)

    fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=220)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fafbfa")

    bars = ax.barh(df_top["Destination"], df_top["Growth_2022_2024"],
                   color=["#3b7a5e"] * 6 + ["#b8922a", "#154734"],
                   height=0.62, edgecolor="#12382a", linewidth=0.6)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 2.5, bar.get_y() + bar.get_height() / 2, f"+{w:.1f}%",
                va="center", ha="left", fontsize=9, fontweight="bold", color="#1a2620")

    ax.set_xlim(0, 125)
    ax.set_xlabel("Visitor Footfall Growth 2022–2024 (%)", fontsize=10, fontweight="bold", color="#1a2620", labelpad=8)
    ax.set_title("Top Tourist Footfall Expansion Corridors", fontsize=12, fontweight="bold", color="#154734", pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.5, color="#cdd7d0")
    ax.tick_params(colors="#1a2620", labelsize=9.5)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    chart_path = ASSETS_DIR / "chart_visitor_growth.png"
    plt.savefig(chart_path, dpi=220, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"Saved: {chart_path}")

# -------------------------------------------------------------
# 2. Opportunity Quadrants Scatter Plot
# -------------------------------------------------------------
def make_quadrant_chart():
    df_opp = pd.read_csv("08_Results/final_business_opportunity_analysis.csv")

    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=220)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fafbfa")

    x = df_opp["Growth_2022_2024"]
    y = df_opp["Overall_Gap_Score"]

    # Quadrant background tints
    # x: -30 to 125, y: -200 to 160
    ax.axvline(0, color="#8a9a90", linestyle="--", linewidth=0.9, alpha=0.7)
    ax.axhline(0, color="#8a9a90", linestyle="--", linewidth=0.9, alpha=0.7)

    # Shaded quadrants
    ax.fill_between([0, 130], 0, 170, color="#e8f5ec", alpha=0.6, label="High Gap + Pos Growth (Primary Target)")
    ax.fill_between([0, 130], -200, 0, color="#edf4fa", alpha=0.5, label="Low Gap + Pos Growth (Differentiation)")
    ax.fill_between([-40, 0], 0, 170, color="#fdf2f2", alpha=0.5, label="High Gap + Neg Growth (Turnaround)")
    ax.fill_between([-40, 0], -200, 0, color="#f5f5f5", alpha=0.6, label="Low Gap + Neg Growth (Consolidation)")

    colors = []
    for g, gap in zip(x, y):
        if gap > 0 and g > 0:
            colors.append("#2b8a62")
        elif gap <= 0 and g > 0:
            colors.append("#2b6cb0")
        elif gap > 0 and g <= 0:
            colors.append("#d9534f")
        else:
            colors.append("#718096")

    scatter = ax.scatter(x, y, c=colors, s=70, edgecolors="#154734", linewidth=0.8, zorder=4)

    # Annotate key destinations
    highlight_dests = ["Munnar", "Kumarakom", "Vagamon", "Thekkady", "Varkala", "Kozhikode City", "Kochi City", "Silent Valley"]
    for _, row in df_opp.iterrows():
        name = row["Destination"]
        if name in highlight_dests:
            ax.annotate(name, (row["Growth_2022_2024"], row["Overall_Gap_Score"]),
                        textcoords="offset points", xytext=(5, 4), fontsize=8.5,
                        fontweight="bold", color="#12382a",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor="#c5d3c8", linewidth=0.5))

    ax.set_xlabel("Visitor Footfall Growth 2022–2024 (%)", fontsize=10, fontweight="bold", color="#1a2620")
    ax.set_ylabel("Cluster-Relative Infrastructure Gap Score", fontsize=10, fontweight="bold", color="#1a2620")
    ax.set_title("2×2 Strategic Business Opportunity Quadrants", fontsize=12, fontweight="bold", color="#154734", pad=10)
    ax.set_xlim(-30, 125)
    ax.set_ylim(-195, 155)
    ax.grid(True, linestyle=":", alpha=0.5, color="#cbd5cc")

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    chart_path = ASSETS_DIR / "chart_opportunity_quadrants.png"
    plt.savefig(chart_path, dpi=220, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"Saved: {chart_path}")

# -------------------------------------------------------------
# 3. Model Benchmark Comparison Chart
# -------------------------------------------------------------
def make_model_chart():
    models = ["StandardScaler\n+ K-Means", "RobustScaler\n+ K-Means", "RobustScaler + PCA\n+ K-Means"]
    silhouette = [0.3899, 0.5804, 0.6799]
    db_index = [0.9875, 0.6431, 0.5692]

    x = np.arange(len(models))
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(6.2, 4.0), dpi=220)
    fig.patch.set_facecolor("#ffffff")
    ax1.set_facecolor("#fafbfa")

    rects1 = ax1.bar(x - width/2, silhouette, width, label="Silhouette Score (Higher is better)",
                     color="#154734", edgecolor="#0e2a1e", linewidth=0.7)
    
    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, db_index, width, label="Davies-Bouldin Index (Lower is better)",
                     color="#b8922a", edgecolor="#7a6018", linewidth=0.7)

    ax1.set_ylabel("Silhouette Score", fontsize=10, fontweight="bold", color="#154734")
    ax2.set_ylabel("Davies-Bouldin Index", fontsize=10, fontweight="bold", color="#b8922a")
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=9.5, fontweight="bold", color="#1a2620")
    ax1.set_ylim(0, 0.85)
    ax2.set_ylim(0, 1.25)
    ax1.grid(axis="y", linestyle="--", alpha=0.5, color="#cdd7d0")

    # Add data labels
    for r in rects1:
        h = r.get_height()
        ax1.text(r.get_x() + r.get_width()/2., h + 0.02, f"{h:.4f}",
                 ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#154734")

    for r in rects2:
        h = r.get_height()
        ax2.text(r.get_x() + r.get_width()/2., h + 0.02, f"{h:.4f}",
                 ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#b8922a")

    ax1.set_title("Machine Learning Clustering Benchmark", fontsize=12, fontweight="bold", color="#154734", pad=12)
    plt.tight_layout()
    chart_path = ASSETS_DIR / "chart_model_benchmark.png"
    plt.savefig(chart_path, dpi=220, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"Saved: {chart_path}")

# -------------------------------------------------------------
# 4. Financial ROI & Payback Comparison Chart
# -------------------------------------------------------------
def make_financial_chart():
    ventures = ["Homestay", "Restaurant", "Resort", "Hotel"]
    capex_lakhs = [25.0, 35.0, 100.0, 75.0]
    roi_pct = [40.8, 37.7, 27.6, 27.2]
    payback_yrs = [2.5, 2.7, 3.6, 3.7]

    fig, ax1 = plt.subplots(figsize=(6.4, 4.2), dpi=220)
    fig.patch.set_facecolor("#ffffff")
    ax1.set_facecolor("#fafbfa")

    x = np.arange(len(ventures))
    width = 0.36

    rects1 = ax1.bar(x - width/2, roi_pct, width, label="Annual ROI (%)",
                     color="#2b8a62", edgecolor="#154734", linewidth=0.7)

    ax2 = ax1.twinx()
    rects2 = ax2.plot(x + width/2, payback_yrs, marker="o", markersize=8, color="#b8922a",
                      linewidth=2.4, label="Payback Period (Years)")

    ax1.set_ylabel("Annual ROI (%)", fontsize=10, fontweight="bold", color="#2b8a62")
    ax2.set_ylabel("Capital Payback (Years)", fontsize=10, fontweight="bold", color="#b8922a")
    ax1.set_xticks(x)
    ax1.set_xticklabels(ventures, fontsize=10, fontweight="bold", color="#1a2620")
    ax1.set_ylim(0, 50)
    ax2.set_ylim(0, 5.0)
    ax1.grid(axis="y", linestyle="--", alpha=0.5, color="#cdd7d0")

    for r in rects1:
        h = r.get_height()
        ax1.text(r.get_x() + r.get_width()/2., h + 1.0, f"{h:.1f}%",
                 ha="center", va="bottom", fontsize=9, fontweight="bold", color="#154734")

    for i, p in enumerate(payback_yrs):
        ax2.text(x[i] + width/2, p + 0.18, f"{p:.1f} yrs",
                 ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#b8922a")

    ax1.set_title("Hospitality Venture Economics & Payback Horizon", fontsize=12, fontweight="bold", color="#154734", pad=12)
    plt.tight_layout()
    chart_path = ASSETS_DIR / "chart_financial_roi.png"
    plt.savefig(chart_path, dpi=220, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"Saved: {chart_path}")

if __name__ == "__main__":
    make_growth_chart()
    make_quadrant_chart()
    make_model_chart()
    make_financial_chart()
    print("All charts generated successfully!")
