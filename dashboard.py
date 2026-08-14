import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.title("🚛 SSI Traffic Management Dashboard")

    st.caption(
        "Upload SAP Export → Calculate → Dashboard → Export Report"
    )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Executive",
            "Buyer",
            "Customer",
            "Detail",
            "Move Coil",
            "Planning",
            "Move Form"
        ]
    )

    # =====================================
    # EXECUTIVE
    # =====================================

    with tab1:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Outstanding",
            round(
                df["Outstanding"].sum(),
                2
            )
            if "Outstanding" in df.columns
            else 0
        )

        c2.metric(
            "Production Add",
            round(
                df["Production_Add"].sum(),
                2
            )
            if "Production_Add" in df.columns
            else 0
        )

        c3.metric(
            "NC Coil",
            round(
                df["NC"].sum(),
                2
            )
            if "NC" in df.columns
            else 0
        )

        c4.metric(
            "Move Available",
            round(
                df["Move_Available"].sum(),
                2
            )
            if "Move_Available" in df.columns
            else 0
        )

        st.divider()

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Move Coil",
            (
                df["Move_Coil_Result"]
                == "MOVE COIL"
            ).sum()
            if "Move_Coil_Result" in df.columns
            else 0
        )

        m2.metric(
            "Move + Produce",
            (
                df["Move_Coil_Result"]
                == "MOVE + PRODUCE"
            ).sum()
            if "Move_Coil_Result" in df.columns
            else 0
        )

        m3.metric(
            "Produce Only",
            (
                df["Move_Coil_Result"]
                == "PRODUCE ONLY"
            ).sum()
            if "Move_Coil_Result" in df.columns
            else 0
        )

        m4.metric(
            "High Priority",
            (
                df["Move_Priority"]
                == "HIGH"
            ).sum()
            if "Move_Priority" in df.columns
            else 0
        )

        st.divider()

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

            fig_move = px.pie(
                move_status,
                names="Status",
                values="Count",
                hole=0.5
            )

            st.plotly_chart(
                fig_move,
                use_container_width=True
            )

        if "Aging_Group" in df.columns:

            aging_df = (
                df["Aging_Group"]
                .value_counts()
                .reset_index()
            )

            aging_df.columns = [
                "Aging",
                "Count"
            ]

            fig_aging = px.pie(
                aging_df,
                names="Aging",
                values="Count",
                hole=0.5
            )

            st.plotly_chart(
                fig_aging,
                use_container_width=True
            )

    # =====================================
    # BUYER
    # =====================================

    with tab2:

        st.subheader(
            "Buyer Scorecard"
        )

        if "Buyer" in df.columns:

            buyer_df = (
                df.groupby("Buyer")
                .agg({
                    "Outstanding": "sum",
                    "Production_Add": "sum",
                    "NC": "sum",
                    "Move_Available": "sum",
                    "Ready_To_Ship": "sum"
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

    # =====================================
    # CUSTOMER
    # =====================================

    with tab3:

        st.subheader(
            "Customer Summary"
        )

        if "End Cust." in df.columns:

            customer_df = (
                df.groupby("End Cust.")
                .agg({
                    "Outstanding": "sum",
                    "Production_Add": "sum",
                    "NC": "sum"
 
