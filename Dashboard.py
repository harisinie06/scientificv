
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Teaching and Learning Dashboard",
    page_icon="📊",
    layout="wide"
)

# Main title
st.title("Teaching and Learning Evaluation Dashboard")

st.markdown("---")

# Introduction
st.header("Welcome to the Dashboard")

st.write("""
This dashboard presents data visualizations based on the
Teaching and Learning Evaluation project.

Use the sidebar to explore the different visualization
pages for each research objective.
""")

st.info("Select an objective from the sidebar to view its visualizations.")

