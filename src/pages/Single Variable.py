import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger()

st.title("Column Distribution")
st.markdown("Select a column to view its data distribution.")

csv_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
logger.debug("Waiting for CSV file upload.")

if csv_file is not None:
    try:
        df: pd.DataFrame = pd.read_csv(csv_file)
        logger.info(
            f"CSV file '{csv_file.name}' successfully read with {df.shape[0]} rows."
        )
    except Exception as e:
        st.error("Error reading the CSV file. Please check its format.")
        logger.error(f"Error reading CSV: {e}")
    else:
        st.subheader("Select Column")
        column = st.selectbox("Column for Distribution", df.columns)
        logger.debug(f"Column selected: {column}")

        st.subheader(f"Distribution for: {column}")
        fig, ax = plt.subplots(figsize=(6, 4))

        try:
            # numeric vs non-numeric column handling
            if pd.api.types.is_numeric_dtype(df[column]):
                sns.histplot(df[column].dropna(), bins=20, kde=True, ax=ax)
                logger.info(f"Plotted histogram for numeric column '{column}'.")
            else:
                df[column].dropna().value_counts().plot.bar(ax=ax)
                logger.info(f"Plotted bar chart for categorical column '{column}'.")
            st.pyplot(fig)
            logger.debug("Plot displayed successfully in Streamlit.")
        except Exception as e:
            st.error("Error generating plot.")
            logger.exception(f"Plot generation failed for column '{column}': {e}")
else:
    st.info("Please upload a CSV file to get started.")
    logger.warning("No CSV file uploaded by user.")
