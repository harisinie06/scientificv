
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------
st.set_page_config(
    page_title="Objective 1 - Income Analysis",
    page_icon="📊",
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
    box-shadow: 0px 2px 5px rgba(0,0,0,0.04);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# TITLE
# ----------------------------------
st.title("📊 Household Income Analysis")
st.markdown("""
Explore average household income across Malaysian states
using interactive visualizations.
""")

st.divider()

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    url = "https://storage.dosm.gov.my/hies/hh_income_district.csv"

    df = pd.read_csv(url)

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    return df

df_income = load_data()

# ----------------------------------
# FILTER DATA
# ----------------------------------
df_income_filtered = df_income[
    df_income["year"].isin([2019, 2022])
].copy()

# ----------------------------------
# DATA TRANSFORMATION
# ----------------------------------
df_income_state = (
    df_income_filtered
    .groupby(["state", "year"])
    .agg(
        avg_income=("income_mean", "mean"),
        median_income=("income_median", "mean"),
        total_districts=("district", "nunique")
    )
    .reset_index()
)

df_income_2022 = df_income_state[
    df_income_state["year"] == 2022
].copy()

# ----------------------------------
# KPI CARDS
# ----------------------------------
st.subheader("Key Statistics")

if not df_income_2022.empty:

    highest_state = df_income_2022.loc[
        df_income_2022["avg_income"].idxmax()
    ]

    lowest_state = df_income_2022.loc[
        df_income_2022["avg_income"].idxmin()
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Household Income (2022)",
        f"RM {df_income_2022['avg_income'].mean():,.0f}"
    )

    col2.metric(
        "Highest Income State",
        highest_state["state"],
        f"RM {highest_state['avg_income']:,.0f}"
    )

    col3.metric(
        "Lowest Income State",
        lowest_state["state"],
        f"RM {lowest_state['avg_income']:,.0f}"
    )

st.divider()

# ----------------------------------
# VISUALIZATION 1: LINE CHART
# ----------------------------------
st.subheader("1. Household Income Trends by State")

fig1 = px.line(
    df_income_state,
    x="year",
    y="avg_income",
    color="state",
    markers=True,
    title="Average Household Income (2019 vs 2022)",
    labels={
        "year": "Year",
        "avg_income": "Average Income (RM)",
        "state": "State"
    }
)

fig1.update_layout(
    template="plotly_white",
    height=550,
    hovermode="x unified",
    legend_title="State"
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ----------------------------------
# VISUALIZATION 2: DONUT CHART
# ----------------------------------
st.subheader("2. Household Income Comparison by State")

if not df_income_2022.empty:

    pie_data = df_income_2022.sort_values(
        "avg_income",
        ascending=False
    )

    fig2 = px.pie(
        pie_data,
        names="state",
        values="avg_income",
        hole=0.45,
        title="Relative Share of Aggregated State Average Income (2022)",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig2.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Average income: RM %{value:,.0f}<br>"
            "Relative share: %{percent}"
            "<extra></extra>"
        )
    )

    fig2.update_layout(
        template="plotly_white",
        height=550,
        legend_title="State"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.caption(
        "Note: The donut chart compares each state's average "
        "district income relative to the sum of state averages. "
        "It does not represent the actual share of national income."
    )

st.divider()

# ----------------------------------
# VISUALIZATION 3: BAR CHART
# ----------------------------------
st.subheader("3. Income Ranking by State (2022)")

if not df_income_2022.empty:

    bar_data = df_income_2022.sort_values(
        "avg_income",
        ascending=True
    )

    fig3 = px.bar(
        bar_data,
        x="avg_income",
        y="state",
        orientation="h",
        text="avg_income",
        title="Average Household Income Ranking",
        labels={
            "avg_income": "Average Income (RM)",
            "state": "State"
        },
        color="avg_income",
        color_continuous_scale="Blues"
    )

    fig3.update_traces(
        texttemplate="RM %{text:,.0f}",
        textposition="outside"
    )

    fig3.update_layout(
        template="plotly_white",
        height=650,
        coloraxis_showscale=False
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ----------------------------------
# VISUALIZATION 4: HEATMAP
# ----------------------------------
st.subheader("4. Household Income Heatmap")

income_pivot = df_income_state.pivot(
    index="state",
    columns="year",
    values="avg_income"
)

fig4 = px.imshow(
    income_pivot,
    text_auto=".0f",
    aspect="auto",
    color_continuous_scale="YlGnBu",
    title="Average Household Income by State and Year",
    labels={
        "x": "Year",
        "y": "State",
        "color": "Average Income (RM)"
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

st.markdown("""
The visualizations provide a comparison of average household
income across Malaysian states.

The line chart highlights income differences between years.
The donut chart compares the relative values of state averages.
The bar chart ranks states by average income, while the heatmap
shows income patterns across states and years.
""")


