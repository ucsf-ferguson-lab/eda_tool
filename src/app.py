import streamlit as st
import pandas as pd
import math

app_name: str = "Dataset explorer tool"

st.set_page_config(page_title=app_name, layout="wide")
st.title(app_name)
st.markdown("Upload csv, view summary statistics and missing values.")

csv_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if csv_file is not None:
    df: pd.DataFrame = pd.read_csv(csv_file)
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

    # todo: add for non-int cols
    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    # null counts
    st.subheader("Missing Values by Column")
    missing_df: pd.DataFrame = pd.DataFrame(
        {"Missing Count": df.isnull().sum(), "Missing (%)": df.isnull().mean() * 100}
    )
    st.dataframe(missing_df)
else:
    st.info("Please upload a CSV file to get started.")
