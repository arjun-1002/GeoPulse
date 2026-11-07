
import pandas as pd
import matplotlib.pyplot as plt
import os
import calendar

# Load Google Trends data
data = pd.read_csv(
    "data/kerala_tourism_master_long.csv"
)

# Convert date column
data["Time"] = pd.to_datetime(data["Time"])

# Keep complete years only
data = data[
    (data["Time"].dt.year >= 2022) &
    (data["Time"].dt.year <= 2025)
].copy()

# Extract calendar month
data["Month"] = data["Time"].dt.month

# Calculate average interest for each destination and month
monthly = (
    data.groupby(["destination", "Month"])["interest"]
    .mean()
    .reset_index()
)

# Calculate seasonal index within each destination
monthly["Seasonal_Index"] = (
    monthly["interest"] /
    monthly.groupby("destination")["interest"].transform("mean")
) * 100

# Add month names
monthly["Month_Name"] = monthly["Month"].apply(
    lambda x: calendar.month_name[x]
)

# Create results folder
os.makedirs("results", exist_ok=True)

# Save monthly results
monthly.to_csv(
    "results/seasonal_monthly_analysis.csv",
    index=False
)

# Create summary for every destination
summary = []

for destination in monthly["destination"].unique():

    destination_data = monthly[
        monthly["destination"] == destination
    ]

    highest = destination_data.loc[
        destination_data["Seasonal_Index"].idxmax()
    ]

    lowest = destination_data.loc[
        destination_data["Seasonal_Index"].idxmin()
    ]

    summary.append({
        "Destination": destination,
        "Highest_Search_Month": highest["Month_Name"],
        "Highest_Seasonal_Index": round(
            highest["Seasonal_Index"], 2
        ),
        "Lowest_Search_Month": lowest["Month_Name"],
        "Lowest_Seasonal_Index": round(
            lowest["Seasonal_Index"], 2
        )
    })

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    "results/seasonal_summary.csv",
    index=False
)

# Generate one chart for each destination
for destination in monthly["destination"].unique():

    destination_data = monthly[
        monthly["destination"] == destination
    ].sort_values("Month")

    plt.figure(figsize=(10, 5))

    plt.plot(
        destination_data["Month_Name"],
        destination_data["Seasonal_Index"],
        marker="o"
    )

    plt.axhline(
        y=100,
        linestyle="--",
        label="Destination average"
    )

    plt.title(
        destination + " - Seasonal Search Interest"
    )

    plt.xlabel("Month")
    plt.ylabel("Seasonal Index")

    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filename = destination.lower() + "_seasonal.png"

    plt.savefig("results/" + filename)
    plt.close()

print("\nSEASONAL ANALYSIS COMPLETED")

print("\nDestination Seasonal Summary:")

print(summary_df.to_string(index=False))

print("\nFiles saved inside the results folder.")
