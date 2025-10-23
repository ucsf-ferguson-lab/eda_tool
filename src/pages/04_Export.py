import streamlit as st
import base64
import logging

st.title("Download HTML Report")
logger = logging.getLogger()

if "summary_stats" in st.session_state and "plot_images" in st.session_state:
    stats_html = st.session_state.summary_stats.to_html()
    null_count_html = st.session_state.null_counts.to_html()
    logger.debug("Loaded stats and null counts df from session state")

    # embed images as base64 into HTML
    img_html_parts = []
    for img_bytes in st.session_state.plot_images:
        encoded = base64.b64encode(img_bytes).decode()
        img_html_parts.append(
            f'<img src="data:image/png;base64,{encoded}" style="max-width:600px;"><br>'
        )
    images_html = "\n".join(img_html_parts)

    full_html = f"""
    <html>
        <head>
            <title>Summary Report</title>
        </head>
        
        <body>
            <h1>Summary Statistics</h1>
                {stats_html}
            <h1>Missingness Count</h1>
                {null_count_html}
            <h1>Variable Distributions</h1>
                {images_html}
        </body>
    </html>
    """
    logger.debug("Html generated")

    st.download_button(
        label="Download HTML Report",
        data=full_html,
        file_name="summary_report.html",
        mime="text/html",
    )
else:
    st.info("Upload a CSV file first to generate report content.")
