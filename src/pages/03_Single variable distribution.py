import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import logging

st.title("Single Variable Distribution")
logger = logging.getLogger()

if "df" in st.session_state:
    df = st.session_state.df
    column = st.selectbox("Select a column to plot", options=df.columns)
    if column:
        fig, ax = plt.subplots(figsize=(6, 4))
        logger.debug("Showing all variables distribution plots")

        try:
            if pd.api.types.is_numeric_dtype(df[column]):
                sns.histplot(df[column].dropna(), bins=20, kde=True, ax=ax)
            else:
                df[column].dropna().value_counts().plot.bar(ax=ax)
            ax.set_xlabel(column)
            plt.tight_layout()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Failed to plot column {column}: {e}")
            logger.error(f"Failed to plot column {column}")
else:
    st.info("Upload a CSV file in the sidebar to enable this feature.")
