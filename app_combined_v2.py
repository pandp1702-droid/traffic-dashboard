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

    df = pd.read_excel(uploaded_file)

    result = calculate(df)

# ===== FILTER SECTION =====

st.sidebar.header("Filters")

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
            result["Buyer"].astype(str)
            == buyer
        ]

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

    validation = validate_data(result)

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

    if validation["status"] == "PASS":
        st.success("Validation Passed")
    else:
        st.warning(
            f"Issues Found: {validation['issue_count']}"
        )

        for issue in validation["issues"]:
            st.write(issue)

    show_dashboard(result)

    st.subheader("Detail Data")

    st.dataframe(
        result,
        use_container_width=True
    )

    excel_file = export_to_excel(result)

    st.download_button(
        "Export Excel",
        data=excel_file,
        file_name="Balance_Coil_Result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
