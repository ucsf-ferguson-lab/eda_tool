import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Column Distribution")
st.markdown("Select a column to view its data distribution.")

csv_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if csv_file is not None:
    df: pd.DataFrame = pd.read_csv(csv_file)
    st.subheader("Select Column")
    column = st.selectbox("Column for Distribution", df.columns)

    st.subheader(f"Distribution for: {column}")
    fig, ax = plt.subplots(figsize=(6, 4))

    # switch appropriate plot on column type
    if pd.api.types.is_numeric_dtype(df[column]):
        sns.histplot(df[column].dropna(), bins=20, kde=True, ax=ax)
    else:
        df[column].dropna().value_counts().plot.bar(ax=ax)

    st.pyplot(fig)
else:
    st.info("Please upload a CSV file to get started.")
