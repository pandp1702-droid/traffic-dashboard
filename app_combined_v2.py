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

    validation = validate_data(result)

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
