import streamlit as st
import logging

st.title("All Variables Distribution")
logger = logging.getLogger()

if "df" in st.session_state and "plot_images" in st.session_state:
    for img in st.session_state.plot_images:
        st.image(img, width="stretch")
    logger.debug("Showing all variables distribution plots")
else:
    st.info("Upload a CSV file in sidebar to see variable distributions.")
