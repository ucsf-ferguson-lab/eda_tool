import streamlit as st
import pandas as pd
import logging

st.title("Summary statistics and missingness counts")
logger = logging.getLogger()

if "df" in st.session_state and "summary_stats" in st.session_state:
    st.subheader("Summary Statistics")
    st.dataframe(st.session_state.summary_stats)
    logger.debug("Read csv from session state")

    missing_counts = st.session_state.df.isnull().sum()
    missing_percent = (missing_counts / len(st.session_state.df)) * 100

    missing_df = (
        pd.DataFrame(
            {
                "Missing Count": missing_counts,
                "Missing (%)": missing_percent.round(2),
            }
        )
        .reset_index()
        .rename(columns={"index": "Column"})
    )

    st.subheader("Missing Values by Column")
    st.dataframe(missing_df)

    st.session_state.null_counts = missing_df
    logger.debug("Null counts df generated and saved to session state")
else:
    st.info("Upload a CSV file in sidebar to see summary statistics.")
