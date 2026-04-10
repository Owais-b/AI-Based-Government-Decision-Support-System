import pandas as pd
from sklearn.ensemble import IsolationForest


def compute_daily_trends(df):
    """Compute daily complaint trends"""
    if df.empty:
        return pd.DataFrame()
    # Group by date, borough, and complaint_type
    daily = df.groupby([
        df['created_date'].dt.date, 
        'borough', 
        'complaint_type'
    ]).size().reset_index(name='count')
    return daily

def detect_anomalies(df_grouped):
    """Detect anomalies in complaint counts"""
    if df_grouped.empty or len(df_grouped) < 10:
        df_grouped['anomaly'] = 1
        return df_grouped
    
    model = IsolationForest(contamination=0.05, random_state=42)
    df_grouped = df_grouped.copy()
    df_grouped['anomaly'] = model.fit_predict(df_grouped[['count']].values)
    return df_grouped

def crisis_early_warning(df):
    """Simple crisis early warning based on recent growth"""
    if df.empty:
        return "No sufficient data"
    
    # Take last 14 days
    recent = df[df['created_date'] >= df['created_date'].max() - pd.Timedelta(days=14)]
    if len(recent) < 2:
        return "Normal trend - insufficient data for prediction"
    
    weekly = recent.groupby('complaint_type').size()
    if len(weekly) < 2:
        return "Normal trend"
    
    growth = ((weekly.iloc[-1] - weekly.iloc[0]) / weekly.iloc[0] * 100) if weekly.iloc[0] != 0 else 0
    
    if growth > 40:
        return f"🚨 HIGH RISK: {weekly.index[-1]} complaints rising {growth:.1f}% — possible crisis in 5-7 days"
    elif growth > 20:
        return f"⚠️ Warning: {weekly.index[-1]} complaints rising {growth:.1f}%"
    return "Normal trend"