# officer_app.py
import streamlit as st
import pandas as pd
import plotly.express as px   # This was missing - now added
import os

from modules.data_processor import load_data, get_sample_data
from modules.nlp_engine import classify_complaint
from modules.analytics_engine import compute_daily_trends, crisis_early_warning
from modules.decision_engine import calculate_priority_score, generate_recommendation
from modules.optimizer import resource_optimizer
from modules.simulator import policy_simulator
from modules.copilot import ai_copilot_response
from generate_report import generate_professional_report

st.set_page_config(page_title="Officer Dashboard", layout="wide")
st.title("👨‍💼 AI-Driven Government Decision Intelligence Platform")
st.markdown("**Officer Dashboard** — What should the government do next — and why?")

# Load combined data (original + live citizen complaints)
@st.cache_data
def load_full_data():
    df_original = load_data("data/nyc_dataset.csv")
    try:
        df_live = pd.read_csv("data/live_complaints.csv")
        return pd.concat([df_original, df_live], ignore_index=True)
    except:
        return df_original

df = load_full_data()
df_sample = get_sample_data(df)

# Sidebar Navigation
tab_selection = st.sidebar.radio("Navigate", [
    "📊 Dashboard", "🧠 NLP Analysis", "📈 Analytics & Prediction",
    "⭐ Decision Engine", "💰 Resource Optimizer", "🔮 Policy Simulator",
    "🤖 AI Copilot", "🗺️ Geo Map"
])

if tab_selection == "📊 Dashboard":
    st.subheader("Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Complaints", len(df))
    col2.metric("Open Complaints", len(df[df.get('status', pd.Series()) == 'Open']))
    col3.metric("Avg Resolution Time (hrs)", 
                round(df['resolution_time'].mean(), 1) if 'resolution_time' in df.columns else "N/A")
    col4.metric("Crisis Risk", crisis_early_warning(df))

    # Fixed: px is now imported
    st.plotly_chart(
        px.histogram(df, x="borough", color="agency", 
                     title="Complaints by Borough & Agency"), 
        use_container_width=True
    )

elif tab_selection == "🧠 NLP Analysis":
    st.subheader("NLP Understanding Engine")
    sample = df_sample.head(100).copy()
    sample['sentiment'] = sample.apply(lambda x: classify_complaint(x)['sentiment_score'], axis=1)
    sample['urgency'] = sample.apply(lambda x: classify_complaint(x)['urgency'], axis=1)
    st.dataframe(sample[['complaint_type', 'descriptor', 'sentiment', 'urgency']])

elif tab_selection == "📈 Analytics & Prediction":
    st.subheader("Pattern Intelligence + Crisis Early Warning")
    trends = compute_daily_trends(df_sample)
    st.plotly_chart(
        px.line(trends.groupby('created_date')['count'].sum().reset_index(), 
                x='created_date', y='count', title="Complaint Trend"), 
        use_container_width=True
    )
    st.info(crisis_early_warning(df))

elif tab_selection == "⭐ Decision Engine":
    st.subheader("Decision Recommendation Engine")
    df_sample['priority_score'] = df_sample.apply(calculate_priority_score, axis=1)
    rec = generate_recommendation(df_sample)
    st.markdown(rec)

elif tab_selection == "💰 Resource Optimizer":
    st.subheader("Smart Resource Allocation Optimizer")
    budget = st.slider("Available Budget (₹ Lakh)", 1, 50, 10)
    priorities = {"HPD": 0.45, "DSNY": 0.30, "NYPD": 0.25}
    allocation = resource_optimizer(budget * 100000, priorities)
    st.write("**Recommended Allocation:**")
    for agency, amount in allocation.items():
        st.write(f"• {agency}: ₹{amount:,.0f}")

elif tab_selection == "🔮 Policy Simulator":
    st.subheader("Policy Impact Simulator")
    increase = st.slider("Budget Increase %", 0, 100, 20)
    result = policy_simulator(increase)
    st.success(result["message"])
    st.metric("Expected Complaint Reduction", f"{result['expected_reduction_percent']}%")

elif tab_selection == "🤖 AI Copilot":
    st.subheader("AI Copilot for Officers")
    user_query = st.text_input("Ask anything (e.g. Which area needs urgent attention?)")
    if user_query:
        response = ai_copilot_response(user_query, df_sample)
        st.markdown(response)

elif tab_selection == "🗺️ Geo Map":
    st.subheader("Interactive Complaint Heatmap")
    map_data = df_sample[['latitude', 'longitude']].dropna()
    st.map(map_data)

# ==================== PROFESSIONAL REPORT ====================
st.divider()
if st.button("📄 Generate Professional Weekly PDF Report", type="primary", use_container_width=True):
    with st.spinner("Generating professional report..."):
        os.makedirs("reports", exist_ok=True)
        
        # Get current recommendation
        df_sample = get_sample_data(df)
        df_sample['priority_score'] = df_sample.apply(calculate_priority_score, axis=1)
        rec = generate_recommendation(df_sample)
        
        # Correct call - no 'df' parameter
        output_path = generate_professional_report(
            output_path="reports/weekly_decision_report.pdf",
            total_complaints=len(df),
            recommendation=rec,
            budget=1500000
        )
    
    st.success("✅ Professional Weekly Report Generated!")
    with open(output_path, "rb") as f:
        st.download_button(
            label="⬇️ Download PDF Report",
            data=f,
            file_name="AI_Government_Decision_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.caption("Officer Dashboard | AI assists — Human decides")
