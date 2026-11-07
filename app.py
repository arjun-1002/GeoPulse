from flask import Flask, render_template, send_from_directory, jsonify
from pathlib import Path
import pandas as pd
import json

app = Flask(__name__)
BASE = Path(__file__).resolve().parent
DESTINATIONS = ['Munnar', 'Wayanad', 'Vagamon', 'Thekkady', 'Alappuzha', 'Kumarakom', 'Varkala', 'Kovalam', 'Kochi', 'Kozhikode']

def load_csv(folder, name):
    p = BASE / folder / name
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p)
    except Exception:
        return pd.DataFrame()

def col(df, names):
    for n in names:
        for c in df.columns:
            if str(c).lower().replace(' ', '_') == n.lower().replace(' ', '_'):
                return c
    for n in names:
        for c in df.columns:
            if n.lower().replace(' ', '_') in str(c).lower().replace(' ', '_'):
                return c
    return None

def records(df):
    if df.empty:
        return []
    return json.loads(df.where(pd.notna(df), None).to_json(orient='records'))

@app.route('/')
def index():
    master = load_csv('data', 'kerala_tourism_master_dataset_10_destinations.csv')
    if master.empty:
        master = load_csv('data', 'kerala_tourism_kmeans_input_10_destinations.csv')
    if not master.empty:
        dc = col(master, ['destination'])
        if dc and dc != 'Destination':
            master = master.rename(columns={dc: 'Destination'})
        if 'Destination' in master:
            master = master[master['Destination'].astype(str).str.strip().isin(DESTINATIONS)]

    seasonal = load_csv('results', 'seasonal_monthly_analysis.csv')
    if seasonal.empty:
        seasonal = load_csv('data', 'seasonal_monthly_analysis.csv')

    opportunities = load_csv('results', 'business_opportunity_screening.csv')
    if opportunities.empty:
        opportunities = load_csv('data', 'business_opportunity_screening.csv')

    clusters = load_csv('results', 'destination_clusters.csv')
    if clusters.empty:
        clusters = load_csv('data', 'destination_clusters.csv')

    cluster_summary = load_csv('results', 'cluster_summary.csv')
    if cluster_summary.empty:
        cluster_summary = load_csv('data', 'cluster_summary.csv')

    vc = col(master, ['domestic_visits_2022', 'domestic_visits', 'visits_2022']) if not master.empty else None
    total_visits = int(pd.to_numeric(master[vc], errors='coerce').fillna(0).sum()) if vc else 0

    vc25 = col(master, ['domestic_visits_2025']) if not master.empty else None
    total_visits_2025 = int(pd.to_numeric(master[vc25], errors='coerce').fillna(0).sum()) if vc25 else 0

    business_total = 0
    if not master.empty:
        for names in [['restaurants'], ['cafes']]:
            c = col(master, names)
            if c:
                business_total += int(pd.to_numeric(master[c], errors='coerce').fillna(0).sum())

    total_accommodations = 0
    if not master.empty:
        ac = col(master, ['total_accommodation_listings'])
        if ac:
            total_accommodations = int(pd.to_numeric(master[ac], errors='coerce').fillna(0).sum())

    total_commercial_supply = total_accommodations + business_total

    return render_template(
        'index.html',
        destinations=DESTINATIONS,
        master=records(master),
        seasonal=records(seasonal),
        opportunities=records(opportunities),
        clusters=records(clusters),
        cluster_summary=records(cluster_summary),
        total_visits=total_visits,
        total_visits_2025=total_visits_2025,
        total_accommodations=total_accommodations,
        business_total=business_total,
        total_commercial_supply=total_commercial_supply
    )

@app.route('/results/<path:filename>')
def serve_results(filename):
    return send_from_directory(BASE / 'results', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

