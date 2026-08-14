import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.markdown(
        """
        <style>

        div[data-testid="metric-container"] {
            background-color: #f8f9fa;
            border: 1px solid #d0d7de;
            padding: 15px;
            border-radius: 12px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🚛 SSI Traffic Management Dashboard")

    st.caption(
        "Upload SAP Export → Calculate → Dashboard → Export Report"
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Executive",
            "Buyer",
            "Customer",
            "Detail",
            "Move Coil"
        ]
    )

    # =====================================
    # EXECUTIVE
    # =====================================

    with tab1:

        st.subheader("SSI Traffic KPI")

        k1, k2, k3, k4 = st.columns(4)

        k1.metric(
            "Orders",
            len(df)
        )

        k2.metric(
            "Outstanding",
            round(
                df["Outstanding"].sum(),
                2
            ) if "Outstanding" in df.columns else 0
        )

        k3.metric(
            "Production Add",
            round(
                df["Production_Add"].sum(),
                2
            ) if "Production_Add" in df.columns else 0
        )

        k4.metric(
            "NC Coil",
            round(
                df["NC"].sum(),
                2
            ) if "NC" in df.columns else 0
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
            "Remaining Coil",
            round(
                df["Remaining_Coil"].sum(),
                2
            ) if "Remaining_Coil" in df.columns else 0
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
        # MOVE KPI
        # =====================================

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

        # =====================================
        # MOVE STATUS
        # =====================================

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
                values="Count",
                hole=0.5
            )

            st.plotly_chart(
                fig_move,
                use_container_width=True
            )

        # =====================================
        # AGING
        # =====================================

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

            st.subheader(
                "Aging Dashboard"
            )

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
        # GRADE
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
                .head(20)
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

        # =====================================
       
