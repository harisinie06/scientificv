
import streamlit as st
import pandas as pd


@st.cache_data
def load_data():

    # ==========================================
    # PHASE 1: LOAD DATASETS
    # ==========================================

    df_income = pd.read_parquet(
        "https://storage.dosm.gov.my/hies/hh_income_state.parquet"
    )

    df_marriage = pd.read_parquet(
        "https://storage.dosm.gov.my/demography/marriages_state.parquet"
    )

    df_school = pd.read_parquet(
        "https://storage.data.gov.my/education/schools_district.parquet"
    )

    # Convert dates
    for df in [df_income, df_marriage, df_school]:
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])

    # ==========================================
    # PHASE 2: FILTER DATA (2019–2023)
    # ==========================================

    df_income_filtered = df_income[
        (df_income["date"].dt.year >= 2019) &
        (df_income["date"].dt.year <= 2023)
    ].copy()

    df_marriage_filtered = df_marriage[
        (df_marriage["date"].dt.year >= 2019) &
        (df_marriage["date"].dt.year <= 2023)
    ].copy()

    df_school_filtered = df_school[
        (df_school["date"].dt.year >= 2019) &
        (df_school["date"].dt.year <= 2023)
    ].copy()

    # Extract year
    df_income_filtered["year"] = df_income_filtered["date"].dt.year
    df_marriage_filtered["year"] = df_marriage_filtered["date"].dt.year
    df_school_filtered["year"] = df_school_filtered["date"].dt.year

    # ==========================================
    # PHASE 3: CLEAN MARRIAGE DATA
    # ==========================================

    df_mar_agg = (
        df_marriage_filtered[
            df_marriage_filtered["sex"] == "female"
        ]
        .groupby(["state", "year"])
        .agg({"abs": "sum", "rate": "mean"})
        .reset_index()
    )

    # ==========================================
    # PHASE 4: CLEAN SCHOOL DATA
    # ==========================================

    df_sch_state = (
        df_school_filtered[
            (df_school_filtered["state"] != "Malaysia") &
            (df_school_filtered["district"] == "All Districts")
        ]
        .groupby(["state", "year"])["schools"]
        .sum()
        .reset_index()
    )

    # ==========================================
    # PHASE 5: MERGE DATASETS
    # ==========================================

    merged_data = pd.merge(
        df_income_filtered,
        df_mar_agg,
        on=["state", "year"],
        how="inner"
    )

    merged_data = pd.merge(
        merged_data,
        df_sch_state,
        on=["state", "year"],
        how="inner"
    )

    return (
        df_income_filtered,
        df_marriage_filtered,
        df_school_filtered,
        merged_data
    )

