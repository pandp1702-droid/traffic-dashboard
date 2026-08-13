import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.header("Traffic Dashboard")

    # ==========================
    # KPI
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

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

    col1.metric(
        "Outstanding",
        f"{outstanding:,.2f}"
    )

    col2.metric(
        "Coil Inventory",
        f"{coil_inv:,.2f}"
    )

    col3.metric(
        "Production Add",
        f"{production_add:,.2f}"
    )

    col4.metric(
        "Move Coil",
        f"{move_coil:,.2f}"
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
        "Open Orders",
        (
            df["Order_Status"] == "OPEN"
        ).sum()
        if "Order_Status" in df.columns
        else 0
    )

    st.divider()

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
            "Top 
