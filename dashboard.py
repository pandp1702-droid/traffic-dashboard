import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.header("Traffic Dashboard")

    # ==========================
    # KPI SECTION
    # ==========================

    c1, c2, c3, c4 = st.columns(4)

    outstanding = (
        df["Outstanding"].sum()
        if "Outstanding" in df.columns
        else 0
    )

    coil_inv = (
        df["Coil_Inv"].sum()
        if "Coil_Inv" in df.columns
        else 0
    )

    production_add = (
        df["Production_Add"].sum()
        if "Production_Add" in df.columns
        else 0
    )

    move_coil = (
        df["Move_Coil"].sum()
        if "Move_Coil" in df.columns
        else 0
    )

    c1.metric(
        "Outstanding",
        f"{outstanding:,.2f}"
    )

    c2.metric(
        "Coil Inventory",
        f"{coil_inv:,.2f}"
    )

    c3.metric(
        "Production Add",
        f"{production_add:,.2f}"
    )

    c4.metric(
        "Move Coil",
        f"{move_coil:,.2f}"
    )

    st.divider()

    # ==========================
    # SUMMARY KPI
    # ==========================

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric(
        "Total Orders",
        len(df)
    )

    k2.metric(
        "Total Buyers",
        df["Buyer"].nunique()
        if "Buyer" in df.columns
        else 0
    )

    k3.metric(
        "Total Customers",
        df["End Cust."].nunique()
        if "End Cust." in df.columns
        else 0
    )

    k4.metric(
        "Open Orders",
        (
            df["Order_Status"] == "OPEN"
        ).sum()
        if "Order_Status" in df.columns
        else 0
    )

    k5.metric(
    "Closed Orders",
    (
        df["Order_Status"]
        == "CLOSED"
    ).sum()
    if "Order_Status" in df.columns
    else 0
)
    st.divider()

    # ==========================
    # OUTSTANDING BY BUYER
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

        fig1 = px.bar(
            buyer_df,
            x="Buyer",
            y="Outstanding",
            color="Outstanding",
            title="Outstanding By Buyer"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # ==========================
    # OUTSTANDING BY CUSTOMER
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

        fig2 = px.bar(
            customer_df,
            x="End Cust.",
            y="Outstanding",
            color="Outstanding",
            title="Outstanding By Customer"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # ==========================
    # MOVE COIL BY BUYER
    # ==========================

    if (
        "Buyer" in df.columns
        and "Move_Coil" in df.columns
    ):

        move_df = (
            df.groupby("Buyer")["Move_Coil"]
            .sum()
            .reset_index()
            .sort_values(
                "Move_Coil",
                ascending=False
            )
            .head(10)
        )

        st.subheader(
            "Top 10 Move Coil By Buyer"
        )

        fig3 = px.bar(
            move_df,
            x="Buyer",
            y="Move_Coil",
            color="Move_Coil",
            title="Move Coil By Buyer"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # ==========================
    # ORDER STATUS
    # ==========================

    if "Order_Status" in df.columns:

        status_df = (
            df["Order_Status"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = [
            "Status",
            "Count"
        ]

        st.subheader(
            "Order Status"
        )

        fig4 = px.pie(
            status_df,
            names="Status",
            values="Count",
            hole=0.4
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    st.divider()

    # ==========================
    # DATA PREVIEW
    # ==========================

    st.subheader("Data Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )
