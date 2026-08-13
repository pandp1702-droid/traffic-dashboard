import streamlit as st
import plotly.express as px
import pandas as pd


def show_dashboard(df):

    st.header("Traffic Dashboard")

    # KPI
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

    col1.metric("Outstanding", f"{outstanding:,.2f}")
    col2.metric("Coil Inventory", f"{coil_inv:,.2f}")
    col3.metric("Production Add", f"{production_add:,.2f}")
    col4.metric("Move Coil", f"{move_coil:,.2f}")

    st.divider()

    # Buyer Chart
    if (
        "Buyer" in df.columns
        and "Outstanding" in df.columns
    ):

        buyer_df = (
            df.groupby("Buyer", dropna=False)["Outstanding"]
            .sum()
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
            .head(10)
        )

        st.subheader("Top 10 Outstanding By Buyer")

        fig = px.bar(
            buyer_df,
            x="Buyer",
            y="Outstanding",
            title="Outstanding By Buyer"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Customer Chart
    if (
        "End Cust." in df.columns
        and "Outstanding" in df.columns
    ):

        customer_df = (
            df.groupby("End Cust.", dropna=False)["Outstanding"]
            .sum()
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
            .head(10)
        )

        st.subheader("Top 10 Outstanding By Customer")

        fig = px.bar(
            customer_df,
            x="End Cust.",
            y="Outstanding",
            title="Outstanding By Customer"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Order Status
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

        st.subheader("Order Status")

        fig = px.pie(
            status_df,
            names="Status",
            values="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("Data Preview")
    st.dataframe(
        df.head(100),
        use_container_width=True
    )
