
import streamlit as st
import plotly.express as px
from data import load_data

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.title("Objective 1: Household Income Trends")

st.markdown("""
**Objective:** To visualise how household income changed across
Malaysian states between 2019 and 2022, and to show where it is
highest and lowest.
""")

# ==========================================
# LOAD DATA
# ==========================================

with st.spinner("Loading household income data..."):
    df_income, df_marriage, df_school, merged_data = load_data()

# Use income dataset directly for Objective 1
income_data = df_income[
    (df_income["date"].dt.year >= 2019) &
    (df_income["date"].dt.year <= 2022)
].copy()

income_data["year"] = income_data["date"].dt.year

st.success("Household income data loaded successfully!")

st.divider()

# ==========================================
# VISUALIZATION 1.1
# LINE CHART
# ==========================================

st.subheader("1. Mean Household Income Trends by State")

fig1_1 = px.line(
    income_data,
    x="year",
    y="income_mean",
    color="state",
    markers=True,
    title="Mean Household Income Trajectory by State (2019–2022)",
    labels={
        "income_mean": "Mean Income (RM)",
        "year": "Survey Year",
        "state": "State"
    }
)

fig1_1.update_layout(
    template="plotly_white",
    hovermode="x unified",
    legend_title="Malaysian States"
)

st.plotly_chart(fig1_1, use_container_width=True)

st.divider()

# ==========================================
# VISUALIZATION 1.2
# HORIZONTAL BAR CHART
# ==========================================

st.subheader("2. Highest vs. Lowest Income States")

latest_year = income_data["year"].max()

df_latest = (
    income_data[income_data["year"] == latest_year]
    .sort_values("income_mean", ascending=True)
)

fig1_2 = px.bar(
    df_latest,
    x="income_mean",
    y="state",
    orientation="h",
    color="income_mean",
    color_continuous_scale="Blues",
    title=f"State Ranking by Mean Household Income ({latest_year})",
    labels={
        "income_mean": "Mean Income (RM)",
        "state": "State"
    }
)

fig1_2.update_layout(
    template="plotly_white",
    coloraxis_colorbar_title="Income (RM)"
)

st.plotly_chart(fig1_2, use_container_width=True)

st.divider()

# ==========================================
# VISUALIZATION 1.3
# SCATTER PLOT
# ==========================================

st.subheader("3. Mean vs. Median Household Income")

fig1_3 = px.scatter(
    income_data,
    x="income_median",
    y="income_mean",
    color="state",
    size="income_mean",
    hover_data=["year"],
    title="Mean vs. Median Household Income Distribution (2019–2022)",
    labels={
        "income_median": "Median Income (RM)",
        "income_mean": "Mean Income (RM)",
        "state": "State"
    }
)

fig1_3.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig1_3, use_container_width=True)

st.divider()

st.caption(
    "Data Source: OpenDOSM - Household Income by State"
)
