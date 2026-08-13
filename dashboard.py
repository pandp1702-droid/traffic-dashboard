import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.title("SSI Traffic Dashboard")

    # KPI
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Orders",
        len(df)
    )

    col2.metric(
        "Outstanding",
        round(
            df["Outstanding"].sum(),
            2
        )
        if "Outstanding" in df.columns
        else 0
    )

    col3.metric(
        "Production Add",
        round(
            df["Production_Add"].sum(),
            2
        )
        if "Production_Add" in df.columns
        else 0
    )

    col4.metric(
        "NC Coil",
        round(
            df["NC"].sum(),
            2
        )
        if "NC" in df.columns
        else 0
    )

    st.divider()

    # Move Coil Status
    if "Move_Coil_Result" in df.columns:

        move_status = (
            df["Move_Coil_Result"]
            .value_counts()
            .reset_index()
        )

        move_status.columns = [
            "Status",
            "Count"
        ]

        st.subheader(
            "Move Coil Status"
        )

        fig_move = px.pie(
            move_status,
            names="Status",
            values="Count"
        )

        st.plotly_chart(
            fig_move,
            use_container_width=True
        )

    # Buyer Chart
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
            y="Outstanding"
        )

        st.plotly_chart(
            fig_buyer,
            use_container_width=True
        )

    # Customer Chart
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
            y="Outstanding"
        )

        st.plotly_chart(
            fig_customer,
            use_container_width=True
        )

    st.divider()

    st.subheader("Data Preview")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )
