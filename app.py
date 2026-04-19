import streamlit as st
import pandas as pd

from utils.forecast import generate_forecast
from utils.inventory import calculate_inventory_metrics
from utils.decision import generate_decisions
from utils.llm import generate_insight

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(layout="wide")
st.title("📊 Demand-to-Decision Supply Chain Engine")

# ------------------------
# DESCRIPTION
# ------------------------
st.markdown("""
### 🚀 What this app does
- Forecasts demand
- Optimizes inventory levels
- Detects risks (stockout / overstock)
- Recommends actions

### 🔥 Problem it solves
Companies can forecast demand but struggle to decide:
- What to order
- When to order
- How much to order
""")

# ------------------------
# LOAD DATA
# ------------------------
data = pd.read_csv("data/demo_data.csv")
data['date'] = pd.to_datetime(data['date'])

st.subheader("📂 Data Preview")
st.dataframe(data.head())

# ------------------------
# FORECAST
# ------------------------
data = generate_forecast(data)

st.subheader("📈 Demand Forecast")
st.line_chart(data[['sales', 'forecast']])

# ------------------------
# INVENTORY
# ------------------------
safety_stock, reorder_point, avg_demand = calculate_inventory_metrics(data)

st.subheader("📊 Inventory Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Avg Demand", round(avg_demand, 2))
col2.metric("Reorder Point", round(reorder_point, 2))
col3.metric("Safety Stock", round(safety_stock, 2))

# ------------------------
# DECISION ENGINE
# ------------------------
data = generate_decisions(data, reorder_point, safety_stock)

st.subheader("⚠️ Decisions")
st.dataframe(data[['date', 'inventory', 'decision', 'risk']])

# ------------------------
# GROQ AI
# ------------------------
st.subheader("🤖 AI Insights")

api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if api_key:
    latest = data.iloc[-1]

    with st.spinner("Generating AI insight..."):
        insight = generate_insight(
            api_key,
            latest['inventory'],
            latest['forecast'],
            latest['lead_time']
        )

    st.success(insight)
else:
    st.info("Enter Groq API key to enable AI insights")
