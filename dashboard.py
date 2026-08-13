import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.title("SSI Traffic Dashboard")

    # =====================================
    # SSI KPI
    # =====================================

    st.subheader("SSI Traffic KPI")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Orders",
        len(df)
    )

    k2.metric(
        "Not Produced",
        round(
            df["Not_Produced"].sum(),
            2
        ) if "Not_Produced" in df.columns else 0
    )

    k3.metric(
        "In Production",
        round(
            df["In_Production"].sum(),
            2
        ) if "In_Production" in df.columns else 0
    )

    k4.metric(
        "Problem Coil",
        round(
            df["Problem_Coil"].sum(),
            2
        ) if "Problem_Coil" in df.columns else 0
    )

    k5, k6, k7, k8 = st.columns(4)

    k5.metric(
        "Ready To Ship",
        round(
            df["Ready_To_Ship"].sum(),
            2
        ) if "Ready_To_Ship" in df.columns else 0
    )

    k6.metric(
        "Total Coil",
        round(
            df["Total_Coil"].sum(),
            2
        ) if "Total_Coil" in df.columns else 0
    )

    k7.metric(
        "Outstanding",
        round(
            df["Outstanding"].sum(),
            2
        ) if "Outstanding" in df.columns else 0
    )

    k8.metric(
        "Old Orders",
        (
            df["Old_Order"] == "YES"
        ).sum()
        if "Old_Order" in df.columns
        else 0
    )

    st.divider()

    # =====================================
    # EXECUTIVE KPI
    # =====================================

    e1, e2, e3, e4 = st.columns(4)

    e1.metric(
        "NC Coil",
        round(
            df["NC"].sum(),
            2
        ) if "NC" in df.columns else 0
    )

    e2.metric(
        "Production Add",
        round(
            df["Production_Add"].sum(),
            2
        ) if "Production_Add" in df.columns else 0
    )

    e3.metric(
        "Remaining Coil",
        round(
            df["Remaining_Coil"].sum(),
            2
        ) if "Remaining_Coil" in df.columns else 0
    )

    e4.metric(
        "Move Available",
        round(
            df["Move_Available"].sum(),
            2
        ) if "Move_Available" in df.columns else 0
    )

    st.divider()

    # =====================================
    # MOVE COIL STATUS
    # =====================================

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

    # =====================================
    # BUYER SUMMARY
    # =====================================

    if (
        "Buyer" in df.columns
        and "Outstanding" in df.columns
    ):

        st.subheader(
            "Buyer Summary"
        )

        buyer_df = (
            df.groupby("Buyer")
            .agg({
                "Outstanding": "sum",
                "Production_Add": "sum",
                "NC": "sum"
            })
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
        )

        st.dataframe(
            buyer_df,
            use_container_width=True
        )

        fig_buyer = px.bar(
            buyer_df.head(10),
            x="Buyer",
            y="Outstanding",
            color="Outstanding"
        )

        st.plotly_chart(
            fig_buyer,
            use_container_width=True
        )

    # =====================================
    # CUSTOMER SUMMARY
    # =====================================

    if (
        "End Cust." in df.columns
        and "Outstanding" in df.columns
    ):

        customer_df = (
            df.groupby("End Cust.")
            .agg({
                "Outstanding": "sum",
                "Production_Add": "sum",
                "NC": "sum"
            })
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
        )

        st.subheader(
            "Customer Summary"
        )

        fig_customer = px.bar(
            customer_df.head(10),
            x="End Cust.",
            y="Outstanding",
            color="Outstanding"
        )

        st.plotly_chart(
            fig_customer,
            use_container_width=True
        )

    # =====================================
    # GRADE ANALYSIS
    # =====================================

    if (
        "Com.SG" in df.columns
        and "Outstanding" in df.columns
    ):

        grade_df = (
            df.groupby("Com.SG")
            ["Outstanding"]
            .sum()
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
        )

        st.subheader(
            "Outstanding By Grade"
        )

        fig_grade = px.bar(
            grade_df.head(15),
            x="Com.SG",
            y="Outstanding",
            color="Outstanding"
        )

        st.plotly_chart(
            fig_grade,
            use_container_width=True
        )

    # =====================================
    # HIGH RISK ORDERS
    # =====================================

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

    # =====================================
    # CLOSE ORDER STATUS
    # =====================================

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

    # =====================================
    # DATA PREVIEW
    # =====================================

    st.subheader(
        "Data Preview"
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )
