import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from dotenv import load_dotenv
import logging

from observability.logs import setup_otel_logging

load_dotenv()
setup_otel_logging()
logger = logging.getLogger()
logger.info("App started")

# shared csv uploader, stored in session state
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"], key="csv_upload")

if uploaded_file is not None:
    if (
        "df" not in st.session_state
        or st.session_state.get("uploaded_csv_name", "") != uploaded_file.name
    ):
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.uploaded_csv_name = uploaded_file.name
        logger.debug("Csv name and contents saved to session state")

        st.session_state.summary_stats = df.describe()
        logger.debug("Summary stats generated")

        # generate plots & store as bytes buffers
        plot_images = []
        for col in df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    sns.histplot(df[col].dropna(), bins=20, kde=True, ax=ax)
                else:
                    df[col].dropna().value_counts().plot.bar(ax=ax)
                ax.set_xlabel(col)
                plt.tight_layout()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                plot_images.append(buf.read())
                plt.close(fig)
            except Exception:
                plt.close(fig)
                continue
        st.session_state.plot_images = plot_images
        logger.debug("Plots generated and saved to session state")

st.title("Dataset Explorer Tool")
st.sidebar.info(
    "Use the sidebar to upload a CSV file. Then navigate through the pages."
)

if "df" not in st.session_state:
    st.warning("Please upload a CSV file in the sidebar to get started.")
