# create_live_dataset.py
import pandas as pd
import os

print("Creating empty live_complaints.csv with matching columns...")

# Define the important columns from your original NYC 311 dataset
columns = [
    'unique_key', 'created_date', 'closed_date', 'agency', 'agency_name',
    'complaint_type', 'descriptor', 'descriptor_2', 'location_type',
    'incident_zip', 'incident_address', 'street_name', 'borough',
    'community_board', 'council_district', 'police_precinct',
    'latitude', 'longitude', 'location', 'status', 'resolution_description',
    'resolution_action_updated_date', 'due_date'
]

# Create empty DataFrame with these columns
df_live = pd.DataFrame(columns=columns)

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save as empty CSV (with headers only)
df_live.to_csv("data/live_complaints.csv", index=False)

print("✅ Successfully created 'data/live_complaints.csv'")
print(f"   → Location: {os.path.abspath('data/live_complaints.csv')}")
print(f"   → Number of columns: {len(columns)}")
print("\nYou can now run your main app.")
