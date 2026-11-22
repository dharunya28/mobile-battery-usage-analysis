
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mobile Battery Analysis",
    page_icon="🔋",
    layout="wide"
)

# Load dataset
df = pd.read_csv("mobile_battery.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Title
st.title("🔋 Mobile Battery Usage Pattern Analysis")
st.markdown("### Interactive Mobile Battery Monitoring Dashboard")
st.divider()

# Sidebar filters
st.sidebar.header("Filter Data")

apps = ["All"] + sorted(df["App"].unique().tolist())
selected_app = st.sidebar.selectbox("Select App", apps)

if selected_app != "All":
    filtered_df = df[df["App"] == selected_app]
else:
    filtered_df = df.copy()

# KPI calculations
total_records = len(filtered_df)
avg_screen_time = filtered_df["Screen_Time_Min"].mean()
avg_battery = filtered_df["Battery_Usage"].mean()
top_app = (
    df.groupby("App")["Battery_Usage"]
    .mean()
    .idxmax()
)

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", total_records)
col2.metric("Avg Screen Time", f"{avg_screen_time:.1f} min")
col3.metric("Avg Battery Usage", f"{avg_battery:.1f}%")
col4.metric("Highest Usage App", top_app)

st.divider()

# App-wise battery consumption
st.subheader("📊 App-wise Average Battery Usage")

app_usage = (
    filtered_df.groupby("App", as_index=False)["Battery_Usage"]
    .mean()
)

fig1 = px.bar(
    app_usage,
    x="App",
    y="Battery_Usage",
    color="App",
    text_auto=".1f",
    title="Average Battery Consumption by App"
)
st.plotly_chart(fig1, use_container_width=True)

# Screen time vs battery usage
st.subheader("📱 Screen Time vs Battery Usage")

fig2 = px.scatter(
    filtered_df,
    x="Screen_Time_Min",
    y="Battery_Usage",
    color="App",
    size="Battery_Usage",
    hover_data=["Date"],
    title="Screen Time and Battery Consumption"
)
st.plotly_chart(fig2, use_container_width=True)

# Daily battery usage
st.subheader("📅 Daily Battery Usage")

daily_usage = (
    filtered_df.groupby("Date", as_index=False)["Battery_Usage"]
    .sum()
)

fig3 = px.line(
    daily_usage,
    x="Date",
    y="Battery_Usage",
    markers=True,
    title="Total Battery Usage by Date"
)
st.plotly_chart(fig3, use_container_width=True)

# Detailed dataset
st.subheader("📋 Transaction Details")
st.dataframe(filtered_df, use_container_width=True)

st.caption(
    "Note: This dashboard uses a simulated sample dataset "
    "for educational analysis."
)
