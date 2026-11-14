
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------
st.set_page_config(
    page_title="Objective 1 - Household Income",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# PAGE TITLE
# -----------------------------------
st.title("Objective 1: Household Income Analysis")
st.write(
    "Analysis of average household income across Malaysian "
    "states for 2019 and 2022."
)

st.markdown("---")


# -----------------------------------
# LOAD DATASET
# -----------------------------------
@st.cache_data
def load_data():
    url = "https://storage.dosm.gov.my/hies/hh_income_district.csv"

    df = pd.read_csv(url)

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    return df


df_income = load_data()


# -----------------------------------
# DATA FILTERING
# -----------------------------------
df_income_filtered = df_income[
    df_income["year"].isin([2019, 2022])
].copy()


# -----------------------------------
# DATA TRANSFORMATION
# -----------------------------------
df_income_state = (
    df_income_filtered
    .groupby(["state", "year"])
    .agg(
        avg_district_income_mean=("income_mean", "mean"),
        avg_district_income_median=("income_median", "mean"),
        total_districts=("district", "nunique")
    )
    .reset_index()
)


# -----------------------------------
# DISPLAY DATA
# -----------------------------------
st.subheader("Household Income Dataset")

st.write(
    "The following table shows the average household income "
    "by state and year."
)

st.dataframe(
    df_income_state,
    use_container_width=True
)

st.markdown("---")


# -----------------------------------
# VISUALIZATION 1: LINE CHART
# -----------------------------------
st.subheader("1. Average Household Income Trends by State")

fig1, ax1 = plt.subplots(figsize=(12, 6))

sns.lineplot(
    data=df_income_state,
    x="year",
    y="avg_district_income_mean",
    hue="state",
    marker="o",
    ax=ax1
)

ax1.set_title("Average Household Income by State (2019–2022)")
ax1.set_xlabel("Year")
ax1.set_ylabel("Average Monthly Household Income (RM)")
ax1.legend(
    title="State",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

st.markdown("---")


# -----------------------------------
# VISUALIZATION 2: BAR CHART
# -----------------------------------
st.subheader("2. Highest and Lowest Income States (2022)")

df_income_2022 = df_income_state[
    df_income_state["year"] == 2022
].copy()

df_income_2022 = df_income_2022.sort_values(
    by="avg_district_income_mean",
    ascending=True
)

fig2, ax2 = plt.subplots(figsize=(12, 7))

sns.barplot(
    data=df_income_2022,
    x="avg_district_income_mean",
    y="state",
    ax=ax2
)

ax2.set_title("Average Household Income by State (2022)")
ax2.set_xlabel("Average Monthly Household Income (RM)")
ax2.set_ylabel("State")

plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

st.markdown("---")


# -----------------------------------
# VISUALIZATION 3: HEATMAP
# -----------------------------------
st.subheader("3. Household Income Distribution by State and Year")

income_pivot = df_income_state.pivot(
    index="state",
    columns="year",
    values="avg_district_income_mean"
)

fig3, ax3 = plt.subplots(figsize=(9, 8))

sns.heatmap(
    income_pivot,
    annot=True,
    fmt=".0f",
    cmap="YlGnBu",
    linewidths=0.5,
    ax=ax3
)

ax3.set_title("Average Household Income Heatmap")
ax3.set_xlabel("Year")
ax3.set_ylabel("State")

plt.tight_layout()
st.pyplot(fig3)
plt.close(fig3)


# -----------------------------------
# CONCLUSION
# -----------------------------------
st.markdown("---")

st.subheader("Conclusion")

st.write("""
This analysis compares average household income across
Malaysian states in 2019 and 2022.

The visualizations help identify differences in income
between states, compare changes over time, and examine
the distribution of average household income.
""")

