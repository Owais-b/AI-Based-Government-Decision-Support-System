from datetime import datetime

import numpy as np
import pandas as pd


def load_data(file_path="data/nyc_dataset.csv"):
    """Load and basic cleaning of NYC 311 dataset"""
    try:
        df = pd.read_csv(file_path, low_memory=False)
        
        # Parse dates
        if 'created_date' in df.columns:
            df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
        if 'closed_date' in df.columns:
            df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')
        
        # Calculate resolution time in hours
        if 'closed_date' in df.columns and 'created_date' in df.columns:
            df['resolution_time'] = (df['closed_date'] - df['created_date']).dt.total_seconds() / 3600
        
        # Drop rows with critical missing values
        df = df.dropna(subset=['created_date', 'borough', 'complaint_type'])
        
        print(f"✅ Loaded {len(df)} complaints successfully.")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame()

def get_sample_data(df, n=30000):
    """Return a manageable sample for faster performance"""
    if df.empty:
        return df
    sample_size = min(n, len(df))
    return df.sample(n=sample_size, random_state=42)