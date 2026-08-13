import streamlit as st
import pandas as pd

from calculation import calculate
from validation import validate_data
from dashboard import show_dashboard
from export_excel import export_to_excel


st.set_page_config(
    page_title="SSI Traffic Dashboard",
    layout="wide"
)

st.title("SSI Traffic Dashboard")


uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)


if uploaded_file:

    # =====================================
    # READ FILE
    # =====================================

    df = pd.read_excel(uploaded_file)

    # =====================================
    # CALCULATE
    # =====================================

    result = calculate(df)

    # =====================================
    # FILTER
    # =====================================

    st.sidebar.header("Filters")

    # Buyer

    if "Buyer" in result.columns:

        buyer = st.sidebar.selectbox(
            "Buyer",
            ["All"]
            +
            sorted(
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

    # Customer

    if "End Cust." in result.columns:

        customer = st.sidebar.selectbox(
            "Customer",
            ["All"]
            +
            sorted(
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

    # Grade

    if "Com.SG" in result.columns:

        grade = st.sidebar.selectbox(
            "Grade",
            ["All"]
            +
            sorted(
                result["Com.SG"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        if grade != "All":

            result = result[
                result["Com.SG"]
                .astype(str)
                == grade
            ]

    # Thickness

    if "Thk" in result.columns:

        thk = st.sidebar.selectbox(
            "Thickness",
            ["All"]
            +
            sorted(
                result["Thk"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        if thk != "All":

            result = result[
                result["Thk"]
                .astype(str)
                == thk
            ]

    # Shipment Month

    if "Shipment_Month" in result.columns:

        month = st.sidebar.selectbox(
            "Shipment Month",
            ["All"]
            +
            sorted(
                result["Shipment_Month"]
                .dropna()
                .astype(
