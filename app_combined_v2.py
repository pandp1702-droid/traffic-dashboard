import streamlit as st
import pandas as pd

from calculation import calculate
from validation import validate_data
from dashboard import show_dashboard
from export_excel import export_to_excel


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="SSI Traffic Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================
# HEADER
# =====================================

st.title("🚛 SSI Traffic Management Dashboard")

st.caption(
    "Upload SAP Export → Calculate → Dashboard → Export Report"
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("📌 Navigation")
st.sidebar.markdown("---")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

# =====================================
# PROCESS
# =====================================

if uploaded_file is not None:

    with st.spinner("Loading file..."):

        df = pd.read_excel(uploaded_file)

        result = calculate(df)

    # =====================================
    # FILTERS
    # =====================================

    st.sidebar.header("🔍 Filters")

    # Buyer

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
                .astype(str) == buyer
            ]

    # Customer

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
                .astype(str) == customer
            ]

    # Grade

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
                .astype(str) == grade
            ]

    # Thickness

    if "Thk" in result.columns:

        thickness = st.sidebar.selectbox(
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

        if thickness != "All":

            result = result[
                result["Thk"]
                .astype(str) == thickness
            ]

    # Shipment Month

    if "Shipment_Month" in result.columns:

        shipment_month = st.sidebar.selectbox(
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

        if shipment_month != "All":

            result = result[
                result["Shipment_Month"]
                .astype(str)
                == shipment_month
            ]

    st.sidebar.markdown("---")

    # =====================================
    # SEARCH
    # =====================================

    st.sidebar.header("🔎 Search")

    order_search = st.sidebar.text_input(
        "Order No"
    )

    if (
        order_search
        and "OrderNo" in result.columns
    ):

        result = result[
            result["OrderNo"]
            .astype(str)
            .str.contains(
                order_search,
                case=False,
                na=False
            )
        ]

    product_search = st.sidebar.text_input(
        "Product Code"
    )

    if (
        product_search
        and "Prod Cd" in result.columns
    ):

        result = result[
            result["Prod Cd"]
            .astype(str)
            .str.contains(
                product_search,
                case=False,
                na=False
            )
        ]

    customer_search = st.sidebar.text_input(
        "Customer Search"
    )

    if (
        customer_search
        and "End Cust." in result.columns
    ):

        result = result[
            result["End Cust."]
            .astype(str)
            .str.contains(
                customer_search,
                case=False,
                na=False
            )
        ]

    # =====================================
    # VALIDATION
    # =====================================

    validation = validate_data(result)

    if validation["status"] == "PASS":

        st.success("✅ Validation Passed")

    else:

        st.warning(
            f"⚠ Issues Found : {validation['issue_count']}"
        )

        for issue in validation["issues"]:

            st.write(issue)

    # =====================================
    # DASHBOARD
    # =====================================

    show_dashboard(result)

    # =====================================
    # DETAIL DATA
    # =====================================

    with st.expander(
        "📄 Detail Data",
        expanded=False
    ):

        st.dataframe(
            result,
            use_container_width=True,
            height=600
        )

    # =====================================
    # EXPORT
    # =====================================

    st.markdown("---")

    st.subheader("📥 Export Report")

    excel_file = export_to_excel(result)

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📊 Export Excel",
            data=excel_file,
            file_name="Balance_Coil_Result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:

        csv_file = result.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Export CSV",
            data=csv_file,
            file_name="Balance_Coil_Result.csv",
            mime="text/csv"
        )
