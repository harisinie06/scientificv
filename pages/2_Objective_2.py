
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------
st.set_page_config(
    page_title="Objective 2 - Income and Schools",
    page_icon="🏫",
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
st.title("🏫 Objective 2: Household Income and School Distribution")

st.markdown("""
Explore the relationship between average household income
and the distribution of government primary schools
across Malaysian states.
""")

st.divider()

# ----------------------------------
# LOAD DATASETS
# ----------------------------------
@st.cache_data
def load_data():

    income_url = (
        "https://storage.dosm.gov.my/hies/"
        "hh_income_district.csv"
    )

    school_url = (
        "https://storage.data.gov.my/education/"
        "schools_district.csv"
    )

    df_income = pd.read_csv(income_url)
    df_school = pd.read_csv(school_url)

    df_income["date"] = pd.to_datetime(df_income["date"])
    df_school["date"] = pd.to_datetime(df_school["date"])

    df_income["year"] = df_income["date"].dt.year
    df_school["year"] = df_school["date"].dt.year

    return df_income, df_school


df_income, df_school = load_data()

# ----------------------------------
# FILTER HOUSEHOLD INCOME
# ----------------------------------
df_income_filtered = df_income[
    df_income["year"].isin([2019, 2022])
].copy()

income_state = (
    df_income_filtered
    .groupby(["state", "year"])
    .agg(
        avg_income=("income_mean", "mean"),
        median_income=("income_median", "mean")
    )
    .reset_index()
)

# ----------------------------------
# FILTER PRIMARY GOVERNMENT SCHOOLS
# ----------------------------------
df_school_filtered = df_school[
    (df_school["stage"] == "primary") &
    (df_school["type"] == "Sekolah Rendah Kerajaan") &
    (df_school["district"] == "All Districts") &
    (df_school["year"].isin([2019, 2022]))
].copy()

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
df_objective2 = pd.merge(
    income_state,
    school_state,
    on=["state", "year"],
    how="inner"
)

if df_objective2.empty:
    st.error("No matching data found. Please check the datasets.")
    st.stop()

# ----------------------------------
# YEAR SELECTION
# ----------------------------------
available_years = sorted(df_objective2["year"].unique())

selected_year = st.selectbox(
    "Select Year",
    available_years,
    index=len(available_years) - 1
)

df_selected = df_objective2[
    df_objective2["year"] == selected_year
].copy()

st.divider()

# ----------------------------------
# KPI CARDS
# ----------------------------------
st.subheader("Key Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Household Income",
    f"RM {df_selected['avg_income'].mean():,.0f}"
)

col2.metric(
    "Total Primary Schools",
    f"{df_selected['total_schools'].sum():,.0f}"
)

col3.metric(
    "States Analysed",
    f"{df_selected['state'].nunique()}"
)

st.divider()

# ----------------------------------
# VISUALIZATION 1: SCATTER PLOT
# ----------------------------------
st.subheader("1. Relationship Between Household Income and School Distribution")

fig1 = px.scatter(
    df_selected,
    x="avg_income",
    y="total_schools",
    color="state",
    size="total_schools",
    hover_name="state",
    title="Household Income vs Number of Primary Schools",
    labels={
        "avg_income": "Average Household Income (RM)",
        "total_schools": "Number of Primary Schools",
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
st.subheader("2. Primary School Distribution by State")

bar_data = df_selected.sort_values(
    "total_schools",
    ascending=True
)

fig2 = px.bar(
    bar_data,
    x="total_schools",
    y="state",
    orientation="h",
    text="total_schools",
    color="total_schools",
    color_continuous_scale="Blues",
    title="Number of Government Primary Schools by State",
    labels={
        "total_schools": "Number of Schools",
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
st.subheader("3. Distribution of Primary Schools")

fig3 = px.pie(
    df_selected,
    names="state",
    values="total_schools",
    hole=0.45,
    title="Percentage of Primary Schools by State",
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
# VISUALIZATION 4: HEATMAP
# ----------------------------------
st.subheader("4. Primary School Distribution Across Years")

school_pivot = df_objective2.pivot(
    index="state",
    columns="year",
    values="total_schools"
)

fig4 = px.imshow(
    school_pivot,
    text_auto=".0f",
    aspect="auto",
    color_continuous_scale="YlGnBu",
    title="Primary School Distribution by State and Year",
    labels={
        "x": "Year",
        "y": "State",
        "color": "Number of Schools"
    }
)

fig4.update_layout(
    template="plotly_white",
    height=650
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ----------------------------------
# CONCLUSION
# ----------------------------------
st.subheader("Conclusion")

st.write("""
This analysis compares average household income with
the distribution of government primary schools across
Malaysian states.

The scatter plot explores the relationship between the
two variables, while the bar chart and donut chart
compare school distribution across states.

The heatmap highlights differences in school distribution
between 2019 and 2022.
""")

