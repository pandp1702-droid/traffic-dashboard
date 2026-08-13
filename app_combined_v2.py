import streamlit as st
import pandas as pd

from calculation import calculate
from validation import validate_data
from dashboard import show_dashboard
from export_excel import export_to_excel

st.set_page_config(
    page_title="Traffic Dashboard",
    layout="wide"
)

st.title("Traffic Dashboard")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    # Read Excel
    df = pd.read_excel(uploaded_file)

    # Calculate
    result = calculate(df)

    # ==========================
    # SIDEBAR FILTER
    # ==========================
    st.sidebar.header("Filters")

    # Buyer Filter
    if "Buyer" in result.columns:

        buyer = st.sidebar.selectbox(
            "Buyer",
            ["All"]
            + sorted(
                result["Buyer"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        if buyer != "All":

            result = result[
                result["Buyer"]
                .astype(str)
                == buyer
            ]

    # Customer Filter
    if "End Cust." in result.columns:

        customer = st.sidebar.selectbox(
            "Customer",
            ["All"]
            + sorted(
                result["End Cust."]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        if customer != "All":

            result = result[
                result["End Cust."]
                .astype(str)
                == customer
            ]

    # Search Order
    st.sidebar.header("Search")

    search_order
