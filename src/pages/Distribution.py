import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger()

st.title("Column Distributions")
st.markdown("Upload a CSV file to view data distributions for all columns.")

csv_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
logger.debug("Waiting for CSV file upload.")

if csv_file is not None:
    try:
        df = pd.read_csv(csv_file)
        logger.info(
            f"CSV '{csv_file.name}' loaded with {df.shape[0]} rows and {df.shape[1]} columns."
        )
    except Exception as e:
        st.error("Error reading the CSV file.")
        logger.error(f"Error reading CSV: {e}")
    else:
        st.subheader("Column Distributions")
        for column in df.columns:
            st.markdown(f"#### {column}")
            fig, ax = plt.subplots(figsize=(6, 4))

            try:
                if pd.api.types.is_numeric_dtype(df[column]):
                    sns.histplot(df[column].dropna(), bins=20, kde=True, ax=ax)
                    ax.set_xlabel(column)
                    logger.info(f"Plotted numeric distribution for '{column}'.")
                else:
                    df[column].dropna().value_counts().plot.bar(ax=ax)
                    ax.set_xlabel(column)
                    logger.info(f"Plotted categorical distribution for '{column}'.")
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.error(f"Error plotting column '{column}'.")
                logger.exception(f"Plot failed for column '{column}': {e}")
else:
    st.info("Please upload a CSV file to get started.")
    logger.warning("No CSV file uploaded by user.")
