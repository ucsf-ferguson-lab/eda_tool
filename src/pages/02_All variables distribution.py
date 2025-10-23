import streamlit as st

st.title("All Variables Distribution")

if "df" in st.session_state and "plot_images" in st.session_state:
    for img in st.session_state.plot_images:
        st.image(img, width="stretch")
else:
    st.info("Upload a CSV file in sidebar to see variable distributions.")
