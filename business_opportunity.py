
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load master dataset
data = pd.read_csv(
    "data/kerala_tourism_master_dataset_10_destinations.csv"
)

# Select required columns
data = data[
    [
        "Destination",
        "Domestic_Visits_2022",
        "Total_Accommodation_Listings",
        "Restaurants",
        "Cafes"
    ]
].copy()

# Calculate tourism-to-business ratios
data["Visits_Per_Accommodation"] = (
    data["Domestic_Visits_2022"] /
    data["Total_Accommodation_Listings"].replace(0, pd.NA)
)

data["Visits_Per_Restaurant"] = (
    data["Domestic_Visits_2022"] /
    data["Restaurants"].replace(0, pd.NA)
)

data["Visits_Per_Cafe"] = (
    data["Domestic_Visits_2022"] /
    data["Cafes"].replace(0, pd.NA)
)

# Create output folder
os.makedirs("results", exist_ok=True)

# Rank destinations separately for each category
data["Accommodation_Rank"] = (
    data["Visits_Per_Accommodation"]
    .rank(ascending=False, method="min")
)

data["Restaurant_Rank"] = (
    data["Visits_Per_Restaurant"]
    .rank(ascending=False, method="min")
)

data["Cafe_Rank"] = (
    data["Visits_Per_Cafe"]
    .rank(ascending=False, method="min")
)

# Save results
data.to_csv(
    "results/business_opportunity_screening.csv",
    index=False
)

# Accommodation opportunity screening chart
def create_chart(column, title, filename):
    chart_data = data.sort_values(column, ascending=False)

    plt.figure(figsize=(10, 6))
    plt.bar(
        chart_data["Destination"],
        chart_data[column]
    )

    plt.title(title)
    plt.xlabel("Tourism Destinations")
    plt.ylabel("Tourist Visits per Listed Business")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("results/" + filename)
    plt.show()

create_chart(
    "Visits_Per_Accommodation",
    "Accommodation Supply Screening",
    "accommodation_opportunity.png"
)

create_chart(
    "Visits_Per_Restaurant",
    "Restaurant Supply Screening",
    "restaurant_opportunity.png"
)

create_chart(
    "Visits_Per_Cafe",
    "Cafe Supply Screening",
    "cafe_opportunity.png"
)

print("\nBUSINESS OPPORTUNITY SCREENING RESULTS")

print(
    data[
        [
            "Destination",
            "Visits_Per_Accommodation",
            "Visits_Per_Restaurant",
            "Visits_Per_Cafe"
        ]
    ].round(2).to_string(index=False)
)

print("\nResults saved successfully!")
