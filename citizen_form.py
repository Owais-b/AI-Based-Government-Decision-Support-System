# citizen_form.py
import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os

st.title("🗣️ Submit Your Complaint - NYC 311")
st.write("Your complaint will be added to the system for government officers.")

# Load historical data for fake complaint detection
@st.cache_data
def load_historical():
    return pd.read_csv("data/nyc_dataset.csv", low_memory=False)

df_hist = load_historical()

with st.form("citizen_complaint_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *")
        phone = st.text_input("Mobile Number *")
        borough = st.selectbox("Borough *", 
            ["MANHATTAN", "BROOKLYN", "BRONX", "QUEENS", "STATEN ISLAND"])
    
    with col2:
        complaint_type = st.selectbox("Complaint Type *", [
            "HEAT/HOT WATER", "WATER LEAK", "NOISE - RESIDENTIAL", 
            "NOISE - COMMERCIAL", "ILLEGAL PARKING", "MISSED COLLECTION", 
            "DIRTY CONDITION", "SNOW OR ICE", "DOOR/WINDOW", "FLOORING/STAIRS", 
            "APPLIANCE", "OTHER"])
        location_type = st.selectbox("Location Type", 
            ["RESIDENTIAL BUILDING", "STREET/SIDEWALK", "Store/Commercial", "Other"])

    description = st.text_area("Detailed Description of the Problem *", height=100)
    address = st.text_input("Street Address / Landmark (optional)")

    st.write("**Select Exact Location on Map**")
    map_data = pd.DataFrame({"lat": [40.7128], "lon": [-74.0060]})
    st.map(map_data, zoom=10)

    col_lat, col_lon = st.columns(2)
    with col_lat:
        lat = st.number_input("Latitude", value=40.7128, format="%.6f")
    with col_lon:
        lon = st.number_input("Longitude", value=-74.0060, format="%.6f")

    submitted = st.form_submit_button("Submit Complaint", type="primary")

if submitted:
    if not name or not phone or not description or not borough:
        st.error("Please fill all required fields marked with *")
    else:
        # Historical pattern check
        hist_count = len(df_hist[
            (df_hist['borough'] == borough) & 
            (df_hist['complaint_type'] == complaint_type)
        ])
        
        is_suspicious = hist_count < 3
        reason = f"Only {hist_count} similar complaints recorded in {borough} historically." if is_suspicious else ""

        new_complaint = {
            "unique_key": random.randint(60000000, 99999999),
            "created_date": datetime.now().isoformat(),
            "agency": "HPD" if any(x in complaint_type for x in ["HEAT", "WATER", "LEAK"]) else 
                      "DSNY" if "COLLECTION" in complaint_type or "DIRTY" in complaint_type else "NYPD",
            "complaint_type": complaint_type,
            "descriptor": description,
            "location_type": location_type,
            "borough": borough,
            "latitude": lat,
            "longitude": lon,
            "status": "Open",
            "city": borough
        }

        os.makedirs("data", exist_ok=True)
        try:
            live_df = pd.read_csv("data/live_complaints.csv")
        except:
            live_df = pd.DataFrame(columns=new_complaint.keys())
        
        live_df = pd.concat([live_df, pd.DataFrame([new_complaint])], ignore_index=True)
        live_df.to_csv("data/live_complaints.csv", index=False)

        st.success(f"✅ Complaint Submitted! ID: **{new_complaint['unique_key']}**")
        if is_suspicious:
            st.warning(f"⚠️ Flagged for review: {reason}")
        else:
            st.info("Your complaint has been added and will appear in the officer dashboard.")
