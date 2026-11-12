KERALA TOURISM INTELLIGENCE FRONTEND

Copy the 12_Frontend folder into the root of your existing TOURISM INTELLIGENCE project.
Keep 03_Cleaned_Data, 06_EDA_Analysis, 07_Machine_Learning and 08_Results beside it.

From the project root, run:

.\.venv\Scripts\Activate.ps1
pip install -r 12_Frontend/requirements.txt
streamlit run 12_Frontend/app.py

Expected master file:
03_Cleaned_Data/kerala_tourism_master_dataset_25_destinations.csv

Optional supporting files:
06_EDA_Analysis/visitor_growth_2022_2024.csv
07_Machine_Learning/kerala_tourism_cluster_assignments.csv
08_Results/final_business_opportunity_analysis.csv
08_Results/original_cluster_profiles.csv

The app uses existing CSV data. Some pages will show reduced information if optional result files are absent.
Financial calculations use user-entered assumptions. Visitor records and infrastructure counts retain the limitations described in the project.
