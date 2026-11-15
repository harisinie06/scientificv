
import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.title("Objective 2: School Distribution")

st.markdown("""
**Objective:** To examine the number and distribution of schools
across states, districts and school types from 2019 to 2023.
""")

# ==========================================
# LOAD DATA
# ==========================================

with st.spinner("Loading school data..."):
    df_income, df_marriage, df_school, merged_data = load_data()

# Separate state and district data
df_sch_states_only = df_school[
    (df_school["state"] != "Malaysia") &
    (df_school["district"] == "All Districts")
].copy()

df_sch_districts_only = df_school[
    (df_school["state"] != "Malaysia") &
    (df_school["district"] != "All Districts")
].copy()

# Extract year
df_sch_states_only["year"] = df_sch_states_only["date"].dt.year
df_sch_districts_only["year"] = df_sch_districts_only["date"].dt.year

# Filter 2019–2023
df_sch_states_only = df_sch_states_only[
    df_sch_states_only["year"].between(2019, 2023)
]

df_sch_districts_only = df_sch_districts_only[
    df_sch_districts_only["year"].between(2019, 2023)
]

st.success("School data loaded successfully!")

st.divider()

# ==========================================
# VISUALIZATION 2.1
# STACKED BAR CHART
# ==========================================

st.subheader("1. School Distribution by State and School Type")

df_sch_2023 = df_sch_states_only[
    df_sch_states_only["year"] == 2023
]

fig2_1 = px.bar(
    df_sch_2023,
    x="state",
    y="schools",
    color="type",
    title="School Distribution by State and School Type (2023)",
    labels={
        "schools": "Number of Schools",
        "state": "State",
        "type": "School Type"
    }
)

fig2_1.update_layout(
    template="plotly_white",
    barmode="stack",
    xaxis_tickangle=-45,
    legend_title="School Type"
)

st.plotly_chart(fig2_1, use_container_width=True)

st.divider()

# ==========================================
# VISUALIZATION 2.2
# TOP 15 DISTRICTS BAR CHART
# ==========================================

st.subheader("2. Top 15 Districts by School Count")

top_districts = (
    df_sch_districts_only[
        df_sch_districts_only["year"] == 2023
    ]
    .groupby(["state", "district"])["schools"]
    .sum()
    .reset_index()
    .sort_values("schools", ascending=False)
    .head(15)
)

fig2_2 = px.bar(
    top_districts.sort_values("schools", ascending=True),
    x="schools",
    y="district",
    color="state",
    orientation="h",
    title="Top 15 Administrative Districts by Total School Count (2023)",
    labels={
        "schools": "Total Schools",
        "district": "District",
        "state": "State"
    }
)

fig2_2.update_layout(
    template="plotly_white",
    yaxis_title="District",
    legend_title="State"
)

st.plotly_chart(fig2_2, use_container_width=True)

st.divider()

# ==========================================
# VISUALIZATION 2.3
# HEATMAP
# ==========================================

st.subheader("3. Total Schools by State Across Years")

sch_pivot = df_sch_states_only.pivot_table(
    index="state",
    columns="year",
    values="schools",
    aggfunc="sum"
)

fig2_3 = px.imshow(
    sch_pivot,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Viridis",
    title="Heatmap of Total Schools by State (2019–2023)",
    labels={
        "x": "Year",
        "y": "State",
        "color": "Total Schools"
    }
)

fig2_3.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig2_3, use_container_width=True)

st.divider()

st.caption(
    "Data Source: data.gov.my - Schools by Administrative District"
)
