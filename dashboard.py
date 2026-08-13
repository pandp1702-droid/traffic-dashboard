import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.title("SSI Traffic Dashboard")

    # ==========================
    # KPI
    # ==========================

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Outstanding",
        round(
            df["Outstanding"].sum(),
            2
        )
        if "Outstanding" in df.columns
        else 0
    )

    k2.metric(
        "Coil Inventory",
        round(
            df["Coil_Inv"].sum(),
            2
        )
        if "Coil_Inv" in df.columns
        else 0
    )

    k3.metric(
        "Production Add",
        round(
            df["Production_Add"].sum(),
            2
        )
        if "Production_Add" in df.columns
        else 0
    )

    k4.metric(
        "Move Available",
        round(
            df["Move_Available"].sum(),
            2
        )
        if "Move_Available" in df.columns
        else 0
    )

    st.divider()

    # ==========================
    # SUMMARY KPI
    # ==========================

    s1, s2, s3, s4 = st.columns(4)

    s1.metric(
        "Total Orders",
        len(df)
    )

    s2.metric(
        "Total Buyers",
        df["Buyer"].nunique()
        if "Buyer" in df.columns
        else 0
    )

    s3.metric(
        "Total Customers",
        df["End Cust."].nunique()
        if "End Cust." in df.columns
        else 0
    )

    s4.metric(
        "NC Coil",
        round(
            df["NC"].sum(),
            2
        )
        if "NC" in df.columns
        else 0
    )

    st.divider()

    # ==========================
    # MOVE COIL STATUS
    # ==========================

    if "Move_Coil_Result" in df.columns:

        st.subheader(
            "Move Coil Status"
        )

        move_status = (
            df["Move_Coil_Result"]
            .value_counts()
            .reset_index()
        )

        move_status.columns = [
            "Status",
            "Count"
        ]

        fig_move = px.pie(
            move_status,
            names="Status",
            values="Count",
            hole=0.4
        )

        st.plotly_chart(
            fig_move,
            use_container_width=True
        )

    # ==========================
    # TOP BUYER
    # ==========================

    if (
        "Buyer" in df.columns
        and "Outstanding" in df.columns
    ):

        buyer_df = (
            df.groupby("Buyer")["Outstanding"]
            .sum()
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
            .head(10)
        )

        st.subheader(
            "Top 10 Outstanding By Buyer"
        )

        fig_buyer = px.bar(
            buyer_df,
            x="Buyer",
            y="Outstanding",
            color="Outstanding"
        )

        st.plotly_chart(
            fig_buyer,
            use_container_width=True
        )

    # ==========================
    # TOP CUSTOMER
    # ==========================

    if (
        "End Cust." in df.columns
        and "Outstanding" in df.columns
    ):

        customer_df = (
            df.groupby("End Cust.")["Outstanding"]
            .sum()
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
            .head(10)
        )

        st.subheader(
            "Top 10 Outstanding By Customer"
        )

        fig_customer = px.bar(
            customer_df,
            x="End Cust.",
            y="Outstanding",
            color="Outstanding"
        )

        st.plotly_chart(
            fig_customer,
            use_container_width=True
        )

    # ==========================
    # GRADE ANALYSIS
    # ==========================

    if (
        "Com.SG" in df.columns
        and "Outstanding" in df.columns
    ):

        grade_df = (
            df.groupby("Com.SG")["Outstanding"]
            .sum()
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
            .head(15)
        )

        st.subheader(
            "Outstanding By Grade"
        )

        fig_grade = px.bar(
            grade_df,
            x="Com.SG",
            y="Outstanding",
            color="Outstanding"
        )

        st.plotly_chart(
            fig_grade,
            use_container_width=True
        )

    # ==========================
    # HIGH RISK ORDERS
    # ==========================

    if "High_Risk" in df.columns:

        risk_df = df[
            df["High_Risk"] == "YES"
        ]

        st.subheader(
            "High Risk Orders"
        )

        st.dataframe(
            risk_df.head(100),
            use_container_width=True
        )

    # ==========================
    # ORDER STATUS
    # ==========================

    if "Close_Order" in df.columns:

        status_df = (
            df["Close_Order"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = [
            "Status",
            "Count"
        ]

        st.subheader(
            "Close Order Status"
        )

        fig_status = px.pie(
            status_df,
            names="Status",
            values="Count"
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    st.divider()

    # ==========================
    # DATA PREVIEW
    # ==========================

    st.subheader(
        "Data Preview"
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )
