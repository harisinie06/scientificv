
import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.title("Objective 3: Marriage Trends and Socioeconomic Relationships")

st.markdown("""
**Objective:** To analyse how marriages changed across states and
by sex from 2019 to 2023, and to explore how they relate to
household income.
""")

# ==========================================
# LOAD DATA
# ==========================================

with st.spinner("Loading marriage and income data..."):
    df_income, df_marriage, df_school, merged_data = load_data()

# Extract year
df_marriage_filtered = df_marriage[
    df_marriage["state"] != "Malaysia"
].copy()

df_marriage_filtered["year"] = (
    df_marriage_filtered["date"].dt.year
)

df_marriage_filtered = df_marriage_filtered[
    df_marriage_filtered["year"].between(2019, 2023)
]

st.success("Marriage and socioeconomic data loaded successfully!")

st.divider()

# ==========================================
# VISUALIZATION 3.1
# LINE CHART: MARRIAGES BY SEX
# ==========================================

st.subheader("1. National Registered Marriages by Sex")

mar_by_sex = (
    df_marriage_filtered
    .groupby(["year", "sex"])["abs"]
    .sum()
    .reset_index()
)

fig3_1 = px.line(
    mar_by_sex,
    x="year",
    y="abs",
    color="sex",
    markers=True,
    title="National Registered Marriages by Sex (2019–2023)",
    labels={
        "abs": "Total Marriages",
        "year": "Year",
        "sex": "Sex"
    }
)

fig3_1.update_layout(
    template="plotly_white",
    hovermode="x unified",
    legend_title="Sex"
)

st.plotly_chart(fig3_1, use_container_width=True)

st.divider()

# ==========================================
# VISUALIZATION 3.2
# SCATTER PLOT WITH OLS TRENDLINE
# ==========================================

st.subheader("2. Household Income vs. Marriage Rate")

fig3_2 = px.scatter(
    merged_data,
    x="income_mean",
    y="rate",
    color="state",
    trendline="ols",
    hover_data=["year", "abs"],
    title="Mean Household Income vs. Crude Marriage Rate",
    labels={
        "income_mean": "Mean Household Income (RM)",
        "rate": "Marriage Rate (per 1,000)",
        "state": "State"
    }
)

fig3_2.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig3_2, use_container_width=True)

st.divider()

# ==========================================
# VISUALIZATION 3.3
# CORRELATION HEATMAP
# ==========================================

st.subheader("3. Correlation Between Income, Marriages and Schools")

corr_matrix = merged_data[
    [
        "income_mean",
        "income_median",
        "abs",
        "rate",
        "schools"
    ]
].corr()

fig3_3 = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    title="Pearson Correlation Matrix: Income, Marriages and Schools",
    labels={
        "color": "Correlation"
    }
)

fig3_3.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig3_3, use_container_width=True)

st.divider()

st.caption(
    "Data Sources: OpenDOSM - Household Income and Registered Marriages; "
    "data.gov.my - School Statistics"
)
