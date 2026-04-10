import pandas as pd


def calculate_priority_score(row):
    """Calculate priority score safely"""
    try:
        urgency = str(row.get('urgency', 'Low')).lower()
        urgency_score = 3 if urgency == 'high' else 2 if urgency == 'medium' else 1
        
        sentiment_penalty = row.get('negative_sentiment', 0) * 2
        
        delay = row.get('resolution_time', 0)
        if pd.isna(delay):
            delay = 0
            
        score = (1 * 10) + (urgency_score * 30) + (sentiment_penalty * 20) + (delay * 5)
        return round(score, 1)
    except:
        return 50.0

def generate_recommendation(df_filtered):
    """Generate recommendation with safe column handling"""
    if df_filtered.empty:
        return "No sufficient data to generate recommendation."

    df_filtered = df_filtered.copy()

    # Add priority_score if not present
    if 'priority_score' not in df_filtered.columns:
        df_filtered['priority_score'] = df_filtered.apply(calculate_priority_score, axis=1)

    # Safe aggregation - only use columns that exist
    agg_dict = {'priority_score': 'mean'}
    
    if 'negative_sentiment' in df_filtered.columns:
        agg_dict['negative_sentiment'] = 'sum'
    if 'complaint_type' in df_filtered.columns:
        agg_dict['complaint_type'] = 'count'

    try:
        top = (df_filtered.groupby(['borough', 'complaint_type'])
               .agg(agg_dict)
               .rename(columns={'complaint_type': 'count'})
               .sort_values('priority_score', ascending=False)
               .head(5))
    except:
        # Fallback if grouping fails
        top = df_filtered.groupby('borough').agg({'priority_score': 'mean'}).sort_values('priority_score', ascending=False).head(5)

    if top.empty:
        return "No priority areas identified at the moment."

    # Build recommendation text
    first = top.iloc[0]
    borough = top.index[0][0] if isinstance(top.index[0], tuple) else top.index[0]
    issue = top.index[0][1] if isinstance(top.index[0], tuple) else "Multiple Issues"

    rec = f"**Priority Area:** {borough}\n"
    rec += f"**Main Issue:** {issue}\n"
    rec += f"**Priority Score:** {first['priority_score']:.1f}\n"
    
    if 'count' in first:
        rec += f"**Number of Complaints:** {int(first['count'])}\n"
    
    rec += "\n**Suggested Action:** Increase maintenance resources by 20-30% in this area and deploy additional field teams immediately."

    return rec