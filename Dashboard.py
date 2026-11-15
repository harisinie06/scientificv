import streamlit as st

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------
st.set_page_config(
    page_title="Malaysia Data Analysis Dashboard",
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

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
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
# MAIN TITLE
# ----------------------------------
st.title("📊 Malaysia Data Analysis and Visualization Dashboard")

st.markdown("""
### OPEN DOSM DATA | INTERACTIVE VISUALIZATION

Explore the patterns and relationships between
household income, marriage trends, and school
distribution across Malaysia.
""")

st.divider()

# ----------------------------------
# DASHBOARD OVERVIEW
# ----------------------------------
st.header("Dashboard Overview")

st.write("""
This dashboard presents data analysis and interactive
visualizations using datasets obtained from OpenDOSM.
""")

# ----------------------------------
# OBJECTIVE CARDS
# ----------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### Objective 1

    **Marriage and Household Income**

    Explore the relationship between marriage trends
    and household income across Malaysian states.
    """)

with col2:
    st.info("""
    ### Objective 2

    **Household Income and School Distribution**

    Examine household income in relation to
    school distribution across states.
    """)

with col3:
    st.info("""
    ### Objective 3

    **Marriage and School Distribution**

    Explore marriage trends and school
    distribution across Malaysian states.
    """)

st.divider()

# ----------------------------------
# DATASETS
# ----------------------------------
st.header("Datasets Used")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Dataset 1", "Household Income")

with col2:
    st.metric("Dataset 2", "Marriage Trends")

with col3:
    st.metric("Dataset 3", "School Distribution")

st.divider()

# ----------------------------------
# FOOTER
# ----------------------------------
st.caption(
    "Scientific Visualisation | OpenDOSM Data | Malaysia"
)
