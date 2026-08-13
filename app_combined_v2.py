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

    # READ EXCEL
    df = pd.read_excel(uploaded_file)

    # CALCULATE
    result = calculate(df)

    # ==========================
    # FILTERS
    # ==========================

    st.sidebar.header("Filters")

    if "Buyer" in result.columns:

        buyer = st.sidebar.selectbox(
            "Buyer",
            ["All"] +
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

    if "End Cust." in result.columns:

        customer = st.sidebar.selectbox(
            "Customer",
            ["All"] +
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

    if "Com.SG" in result.columns:

        grade = st.sidebar.selectbox(
            "Grade",
            ["All"] +
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

    if "Thk" in result.columns:

        thk = st.sidebar.selectbox(
            "Thickness",
            ["All"] +
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

    if "Shipment_Month" in result.columns:

        month = st.sidebar.selectbox(
            "Shipment Month",
            ["All"] +
            sorted(
                result["Shipment_Month"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        if month != "All":

            result = result[
                result["Shipment_Month"]
                .astype(str)
                == month
            ]

    # ==========================
    # SEARCH
    # ==========================

    st.sidebar.header("Search")

    search_order = st.sidebar.text_input(
        "OrderNo"
    )

    if (
        search_order
        and "OrderNo" in result.columns
    ):

        result = result[
            result["OrderNo"]
            .astype(str)
            .str.contains(
                search_order,
                case=False,
                na=False
            )
        ]

    search_product = st.sidebar.text_input(
        "Product Code"
    )

    if (
        search_product
        and "Prod Cd" in result.columns
    ):

        result = result[
            result["Prod Cd"]
            .astype(str)
            .str.contains(
                search_product,
                case=False,
                na=False
            )
        ]

    search_customer = st.sidebar.text_input(
        "Customer Search"
    )

    if (
        search_customer
        and "End Cust." in result.columns
    ):

        result = result[
            result["End Cust."]
            .astype(str)
            .str.contains(
                search_customer,
                case=False,
                na=False
            )
        ]

    # ==========================
    # VALIDATION
    # ==========================

    validation = validate_data(result)

    if validation["status"] == "PASS":

        st.success(
            "Validation Passed"
        )

    else:

        st.warning(
            f"Issues Found : {validation['issue_count']}"
        )

        for issue in validation["issues"]:

            st.write(issue)

    # ==========================
    # DASHBOARD
    # ==========================

    show_dashboard(result)

    # ==========================
    # DETAIL DATA
    # ==========================

    st.subheader("Detail Data")

    st.dataframe(
        result,
        use_container_width=True,
        height=500
    )

    # ==========================
    # EXPORT EXCEL
    # ==========================

    st.subheader("Export Report")

    excel_file = export_to_excel(result)

    st.download_button(
        label="Export Excel",
        data=excel_file,
        file_name="Balance_Coil_Result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ==========================
    # EXPORT CSV
    # ==========================

    csv = result.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Export CSV",
        data=csv,
        file_name="Balance_Coil_Result.csv",
        mime="text/csv"
    )
