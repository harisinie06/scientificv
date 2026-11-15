
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------
st.set_page_config(
    page_title="Objective 3 - Marriage and Schools",
    page_icon="💍",
    layout="wide"
)

# ----------------------------------
# CUSTOM DESIGN
# ----------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F7F9FC;
}
h1, h2, h3 {
    color: #1E293B;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# TITLE
# ----------------------------------
st.title("💍 Objective 3: Marriage Trends and School Distribution")

st.markdown("""
Explore male marriage trends in relation to the distribution
of government primary schools across Malaysian states.
""")

st.divider()

# ----------------------------------
# LOAD DATASETS
# ----------------------------------
@st.cache_data
def load_data():

    marriage_url = (
        "https://storage.dosm.gov.my/demography/"
        "marriages_state.csv"
    )

    school_url = (
        "https://storage.data.gov.my/education/"
        "schools_district.csv"
    )

    df_marriage = pd.read_csv(marriage_url)
    df_school = pd.read_csv(school_url)

    df_marriage["date"] = pd.to_datetime(df_marriage["date"])
    df_school["date"] = pd.to_datetime(df_school["date"])

    df_marriage["year"] = df_marriage["date"].dt.year
    df_school["year"] = df_school["date"].dt.year

    return df_marriage, df_school


df_marriage, df_school = load_data()

# ----------------------------------
# FILTER MALE MARRIAGE DATA
# ----------------------------------
df_marriage_filtered = df_marriage[
    df_marriage["sex"] == "male"
].copy()

# ----------------------------------
# FILTER PRIMARY GOVERNMENT SCHOOLS
# ----------------------------------
df_school_filtered = df_school[
    (df_school["stage"] == "primary") &
    (df_school["type"] == "Sekolah Rendah Kerajaan") &
    (df_school["district"] == "All Districts")
].copy()

# ----------------------------------
# AGGREGATE MARRIAGE DATA
# ----------------------------------
marriage_state = (
    df_marriage_filtered
    .groupby(["state", "year"])
    .agg(
        total_marriages=("abs", "sum"),
        marriage_rate=("rate", "mean")
    )
    .reset_index()
)

# ----------------------------------
# AGGREGATE SCHOOL DATA
# ----------------------------------
school_state = (
    df_school_filtered
    .groupby(["state", "year"])
    .agg(
        total_schools=("schools", "sum")
    )
    .reset_index()
)

# ----------------------------------
# MERGE DATASETS
# ----------------------------------
df_objective3 = pd.merge(
    marriage_state,
    school_state,
    on=["state", "year"],
    how="inner"
)

if df_objective3.empty:
    st.error("No matching data found. Please check the datasets.")
    st.stop()

# ----------------------------------
# YEAR SELECTION
# ----------------------------------
available_years = sorted(df_objective3["year"].unique())

selected_year = st.selectbox(
    "Select Year",
    available_years,
    index=len(available_years) - 1
)

df_selected = df_objective3[
    df_objective3["year"] == selected_year
].copy()

st.divider()

# ----------------------------------
# KPI CARDS
# ----------------------------------
st.subheader("Key Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Male Marriages",
    f"{df_selected['total_marriages'].sum():,.0f}"
)

col2.metric(
    "Total Primary Schools",
    f"{df_selected['total_schools'].sum():,.0f}"
)

col3.metric(
    "Average Male Marriage Rate",
    f"{df_selected['marriage_rate'].mean():.2f}"
)

st.divider()

# ----------------------------------
# VISUALIZATION 1: SCATTER PLOT
# ----------------------------------
st.subheader("1. Relationship Between Marriage Rate and School Distribution")

fig1 = px.scatter(
    df_selected,
    x="total_schools",
    y="marriage_rate",
    color="state",
    size="total_marriages",
    hover_name="state",
    title="Male Marriage Rate vs Number of Primary Schools",
    labels={
        "total_schools": "Number of Primary Schools",
        "marriage_rate": "Male Marriage Rate",
        "total_marriages": "Number of Marriages",
        "state": "State"
    }
)

fig1.update_layout(
    template="plotly_white",
    height=550
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ----------------------------------
# VISUALIZATION 2: BAR CHART
# ----------------------------------
st.subheader("2. Male Marriage Comparison by State")

bar_data = df_selected.sort_values(
    "total_marriages",
    ascending=True
)

fig2 = px.bar(
    bar_data,
    x="total_marriages",
    y="state",
    orientation="h",
    text="total_marriages",
    color="total_marriages",
    color_continuous_scale="Blues",
    title="Number of Male Marriages by State",
    labels={
        "total_marriages": "Number of Marriages",
        "state": "State"
    }
)

fig2.update_traces(
    textposition="outside"
)

fig2.update_layout(
    template="plotly_white",
    height=650,
    coloraxis_showscale=False
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ----------------------------------
# VISUALIZATION 3: DONUT CHART
# ----------------------------------
st.subheader("3. Distribution of Male Marriages")

fig3 = px.pie(
    df_selected,
    names="state",
    values="total_marriages",
    hole=0.45,
    title="Percentage of Male Marriages by State",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig3.update_traces(
    textposition="inside",
    textinfo="percent"
)

fig3.update_layout(
    template="plotly_white",
    height=550
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ----------------------------------
# VISUALIZATION 4: LINE CHART
# ----------------------------------
st.subheader("4. Male Marriage Trends Over Time")

fig4 = px.line(
    df_objective3,
    x="year",
    y="total_marriages",
    color="state",
    markers=True,
    title="Male Marriage Trends Across Malaysian States",
    labels={
        "year": "Year",
        "total_marriages": "Number of Marriages",
        "state": "State"
    }
)

fig4.update_layout(
    template="plotly_white",
    height=550,
    hovermode="x unified"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ----------------------------------
# VISUALIZATION 5: HEATMAP
# ----------------------------------
st.subheader("5. Male Marriage Rate Heatmap")

marriage_pivot = df_objective3.pivot(
    index="state",
    columns="year",
    values="marriage_rate"
)

fig5 = px.imshow(
    marriage_pivot,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="YlGnBu",
    title="Male Marriage Rate by State and Year",
    labels={
        "x": "Year",
        "y": "State",
        "color": "Marriage Rate"
    }
)

fig5.update_layout(
    template="plotly_white",
    height=650
)

st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ----------------------------------
# CONCLUSION
# ----------------------------------
st.subheader("Conclusion")

st.write("""
This analysis examines male marriage trends alongside
the distribution of government primary schools across
Malaysian states.

The scatter plot explores the relationship between
marriage rates and school numbers. The bar and donut
charts compare marriage counts across states, while
the line chart and heatmap show marriage patterns
over time.
""")

