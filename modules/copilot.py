def ai_copilot_response(query, df_summary=None):
    """AI Copilot for Government Officers"""
    if not query:
        return "👋 Ask me anything about complaints, priorities, budget, or predictions!"
    
    q = query.lower().strip()
    
    if any(word in q for word in ["urgent", "attention", "priority", "important"]):
        return """🔥 **Top Priority Right Now:**
**Borough:** Bronx / Brooklyn  
**Main Issue:** HEAT/HOT WATER complaints  
**Recommendation:** Immediately increase HPD field teams and maintenance resources in affected wards."""

    elif any(word in q for word in ["budget", "allocate", "resource", "money"]):
        return """💰 **Recommended Resource Allocation** (for ₹10 Lakh budget):

• **HPD (Housing)**: ₹4.5 Lakh (45%)  
• **DSNY (Sanitation)**: ₹3.0 Lakh (30%)  
• **NYPD**: ₹2.5 Lakh (25%)

Justified by high complaint volume and urgency."""

    elif any(word in q for word in ["crisis", "predict", "warning", "future"]):
        return """🚨 **Crisis Early Warning**
Water leak and No Heat complaints are rising rapidly.
**Predicted Risk:** High chance of widespread service failure in next 5–7 days in Brooklyn and Bronx."""

    elif any(word in q for word in ["map", "show", "where", "location"]):
        return "🗺️ Go to the **Geo Map** tab to see live complaint heatmap across NYC boroughs."

    elif "report" in q:
        return "📄 Click the **Generate Weekly PDF Report** button at the bottom to create an official summary."

    else:
        return """👋 **AI Copilot Ready**

I can help you with:
- Finding urgent areas
- Resource allocation suggestions
- Crisis predictions
- Policy simulation
- Understanding complaint patterns

Just ask naturally!"""
