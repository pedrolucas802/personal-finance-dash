
import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="PLSB DASH",
        page_icon="👋",
    )

    st.write("# Welcome to PLSB dashboard! 👋")

    st.sidebar.success("Select a demo above!")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        However, I'm selfish and egocentrical so I'm going to use for my personal finance and stuff.
    """
    )


if __name__ == "__main__":
    run()
