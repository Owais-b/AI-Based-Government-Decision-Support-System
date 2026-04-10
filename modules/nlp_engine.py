import pandas as pd
from textblob import TextBlob


def get_sentiment(text):
    """Calculate sentiment score"""
    if pd.isna(text) or text is None:
        return 0.0
    try:
        analysis = TextBlob(str(text))
        return analysis.sentiment.polarity
    except:
        return 0.0

def detect_urgency(descriptor):
    """Detect urgency level from complaint description"""
    if pd.isna(descriptor):
        return "Low"
    
    text = str(descriptor).lower()
    high_keywords = ['no heat', 'no water', 'leak', 'flood', 'broken', 'emergency', 'danger', 'collapsed']
    medium_keywords = ['noise', 'parking', 'missed', 'dirty', 'snow']
    
    if any(k in text for k in high_keywords):
        return "High"
    elif any(k in text for k in medium_keywords):
        return "Medium"
    return "Low"

def classify_complaint(row):
    """Classify a single complaint with sentiment and urgency"""
    sentiment_score = get_sentiment(row.get('descriptor'))
    urgency = detect_urgency(row.get('descriptor'))
    
    return {
        "category": row.get('complaint_type', 'Unknown'),
        "sentiment_score": round(sentiment_score, 3),
        "urgency": urgency,
        "negative_sentiment": 1 if sentiment_score < -0.2 else 0
    }