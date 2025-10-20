import streamlit as st
import pandas as pd
import math
from dotenv import load_dotenv
import logging

from observability.logs import setup_otel_logging

load_dotenv()
setup_otel_logging()
logger = logging.getLogger()
logger.info("App started")

app_name: str = "Dataset explorer tool"
st.set_page_config(page_title=app_name, layout="wide")
st.title(app_name)
st.markdown(
    "Upload csv, view summary statistics and missing values.\n[Learn More](https://github.com/ucsf-ferguson-lab/eda_tool)"
)

# store uploaded csv in session state
csv_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if csv_file is not None:
    try:
        if "df" not in st.session_state:
            st.session_state.df = pd.read_csv(csv_file)
            logger.debug("CSV read as pandas DataFrame and stored in session_state")
    except Exception as e:
        st.error("Failed to load CSV. Please check the file format or encoding.")
        logger.error(f"Error reading CSV file: {e}")

# access from session state
if "df" in st.session_state:
    df = st.session_state.df
    st.subheader("Data Preview")

    # pagination
    st.markdown("#### Pagination")
    col1, col2 = st.columns(2)
    with col1:
        rows_per_page: int = st.number_input(
            "Rows per page", min_value=5, max_value=1000, value=20
        )
    with col2:
        total_rows: int = df.shape[0]
        total_pages: int = math.ceil(total_rows / rows_per_page)
        page: int = st.number_input("Page", min_value=1, max_value=total_pages, value=1)

    start_row: int = (page - 1) * rows_per_page
    end_row: int = start_row + rows_per_page
    st.dataframe(df.iloc[start_row:end_row])
    logger.debug(f"Displaying rows {start_row} to {end_row} out of {total_rows}")

    # summary statistics
    st.subheader("Summary Statistics")
    try:
        st.dataframe(df.describe())
    except ValueError as e:
        st.warning("Could not compute summary statistics. Check your data types.")
        logger.warning(f"Summary statistics failed: {e}")

    # missing values
    st.subheader("Missing Values by Column")
    try:
        missing_df: pd.DataFrame = pd.DataFrame(
            {
                "Missing Count": df.isnull().sum(),
                "Missing (%)": df.isnull().mean() * 100,
            }
        )
        st.dataframe(missing_df)
    except Exception as e:
        st.error("Error while analyzing missing values.")
        logger.error(f"Missing value computation failed: {e}")

else:
    st.info("Please upload a CSV file to get started.")
    logger.warning("No file uploaded yet")
