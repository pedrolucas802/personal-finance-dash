
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.logger import get_logger
from streamlit_gsheets import GSheetsConnection

LOGGER = get_logger(__name__)


def set_app_config():
    st.set_page_config(page_title="PLSB", page_icon="💰")
    st.write("# Finances 2024")

def get_connection():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn

def read_data(conn):
    try:
        df = conn.read(
            worksheet="Dashboard",
            ttl="10m",
            usecols=[
                "Month",
                "income",
                "outcome",
                "fixed",
                "shooping",
                "expenses",
                "food",
                "gas",
                "parking",
                "signatures",
                "eva",
                "savings",
                "offer",
            ],
        )
    except Exception as e:
        st.error(f"Error reading data: {e}")
        return None

    df = df.dropna(subset=["Month"])
    return df

def select_month(df):
    option = st.selectbox(
        "Select the month:",
        (df["Month"].unique()),
        index=0,
        placeholder="Select month...",
    )
    return option

def display_data(df, option):
    display_expenses_data(df, option)

def display_expenses_data(df, option):
    row_index = df["Month"].index[df["Month"] == option].tolist()[0]
    values = df.iloc[row_index].tolist()
    delta_values = [0 if option == "January" else df.iloc[row_index-1][i] for i in range(len(values))]


    # st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

    with st.expander("General", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Food", value=f"{values[6]:,.2f}",delta=f"{delta_values[6]:,.2f}", delta_color=get_delta_color(delta_values,values,6))
        with col2:
            st.metric(label="Shopping", value=f"{values[4]:,.2f}", delta=f"{delta_values[4]:,.2f}", delta_color=get_delta_color(delta_values,values,4))
        with col3:
            st.metric(label="Expenses", value=f"{values[5]:,.2f}", delta=f"{delta_values[5]:,.2f}", delta_color=get_delta_color(delta_values,values,5))


    with st.expander("Car", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Gas", value=f"{values[7]:,.2f}",delta=f"{delta_values[7]:,.2f}", delta_color=get_delta_color(delta_values,values,7))
        with col2:
            st.metric(label="Parking", value=f"{values[8]:,.2f}", delta=f"{delta_values[8]:,.2f}", delta_color=get_delta_color(delta_values,values,8))

    with st.expander("Reoccurring", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Fixed", value=f"{values[3]:,.2f}",delta=f"{delta_values[3]:,.2f}", delta_color=get_delta_color(delta_values,values,3))
        with col2:
            st.metric(label="Signatures", value=f"{values[9]:,.2f}", delta=f"{delta_values[9]:,.2f}", delta_color=get_delta_color(delta_values,values,9))


    with st.expander("Investment", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Savings", value=f"{values[11]:,.2f}",delta=f"{delta_values[11]:,.2f}", delta_color=get_delta_color(delta_values,values,11))
        with col2:
            st.metric(label="Offer", value=f"{values[12]:,.2f}", delta=f"{delta_values[12]:,.2f}", delta_color=get_delta_color(delta_values,values,12))

    with st.expander("Expense Breakdown", expanded=True):
        data = {
            "Category": ["Fixed", "Miscellaneous", "Shopping", "Gas", "Parking", "Signature", "Investments"],
            "Amount": [
                values[3],
                get_combined_value(values, 5, 10),
                values[4],
                values[7],
                values[8],
                values[9],
                get_combined_value(values, 11, 12)
            ]
        }

        df = pd.DataFrame(data)
        fig = px.pie(df, values='Amount', names='Category')
        st.plotly_chart(fig)



def get_delta_color(delta_values, values, index):
    return "off" if delta_values[index] == 0.0  else ("inverse" if delta_values[index] < values[index] else "normal")


def get_combined_value(values, index1, index2):
    if len(values) < max(index1, index2) + 1:
        return None
    value1 = values[index1] if index1 < len(values) else None
    value2 = values[index2] if index2 < len(values) else None
    return value1 + value2 if value1 is not None and value2 is not None else None


def main():
    set_app_config()

    try:
        conn = get_connection()
        df = read_data(conn)
        if df is not None:
            option = select_month(df)
            display_data(df, option)
    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()