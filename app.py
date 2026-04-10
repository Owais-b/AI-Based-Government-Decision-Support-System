import os

import pandas as pd
import plotly.express as px
import streamlit as st
from fpdf import FPDF

from modules.analytics_engine import (compute_daily_trends,
                                      crisis_early_warning, detect_anomalies)
from modules.copilot import ai_copilot_response
from modules.data_processor import get_sample_data, load_data
from modules.decision_engine import (calculate_priority_score,
                                     generate_recommendation)
from modules.nlp_engine import classify_complaint, detect_urgency
from modules.optimizer import resource_optimizer
from modules.simulator import policy_simulator

st.set_page_config(page_title="Decision Intelligence Platform", layout="wide")
st.title("🚀 AI-Driven Government Decision Intelligence Platform")
st.markdown("**What should the government do next — and why?** (Human keeps final authority)")

# Load data
@st.cache_data
def get_dataframe():
    return load_data()

df = get_dataframe()
df_sample = get_sample_data(df)

# Sidebar
st.sidebar.header("Controls")
tab_selection = st.sidebar.radio("Navigate", [
    "📊 Dashboard", "🧠 NLP Analysis", "📈 Analytics & Prediction",
    "⭐ Decision Engine", "💰 Resource Optimizer", "🔮 Policy Simulator",
    "🤖 AI Copilot", "🗺️ Geo Map"
])

# ==================== TABS ====================
if tab_selection == "📊 Dashboard":
    st.subheader("Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Complaints", len(df))
    col2.metric("Open Complaints", len(df[df['status'] == 'Open']))
    col3.metric("Avg Resolution Time (hrs)", round(df['resolution_time'].mean(), 1))
    col4.metric("Crisis Risk", crisis_early_warning(df))

    st.plotly_chart(px.histogram(df, x="borough", color="agency", title="Complaints by Borough & Agency"), use_container_width=True)

elif tab_selection == "🧠 NLP Analysis":
    st.subheader("NLP Understanding Engine")
    sample = df_sample.head(100).copy()
    sample['sentiment'] = sample.apply(lambda x: classify_complaint(x)['sentiment_score'], axis=1)
    sample['urgency'] = sample.apply(lambda x: classify_complaint(x)['urgency'], axis=1)
    st.dataframe(sample[['complaint_type', 'descriptor', 'sentiment', 'urgency']])

elif tab_selection == "📈 Analytics & Prediction":
    st.subheader("Pattern Intelligence + Crisis Early Warning")
    trends = compute_daily_trends(df_sample)
    st.plotly_chart(px.line(trends.groupby('created_date')['count'].sum().reset_index(), x='created_date', y='count', title="Complaint Trend"), use_container_width=True)
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

# Auto Report Button
if st.button("📄 Generate Weekly PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weekly Decision Intelligence Report", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Total Complaints: {len(df)}", ln=1)
    pdf.cell(200, 10, txt=generate_recommendation(df_sample), ln=1)
    pdf.output("reports/weekly_report.pdf")
    st.success("Report saved in reports/weekly_report.pdf")
    with open("reports/weekly_report.pdf", "rb") as f:
        st.download_button("Download PDF", f, file_name="weekly_report.pdf")

st.caption("Built as Decision Intelligence Platform | AI assists — Human decides")

