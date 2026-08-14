import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.title("🚛 SSI Traffic Management Dashboard")

    st.caption(
        "Upload SAP Export → Calculate → Dashboard → Export Report"
    )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "ภาพรวม",
            "Buyer",
            "ลูกค้า",
            "ข้อมูล",
            "Move Coil",
            "แผนการผลิต",
            "ฟอร์ม Move Coil"
        ]
    )

    # ==================================================
    # ภาพรวม
    # ==================================================

    with tab1:

        st.subheader("สรุปภาพรวม")

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("จำนวนออร์เดอร์", len(df))

        k2.metric(
            "ค้างส่ง",
            round(df["Outstanding"].sum(), 2)
            if "Outstanding" in df.columns else 0
        )

        k3.metric(
            "ผลิตเพิ่ม",
            round(df["Production_Add"].sum(), 2)
            if "Production_Add" in df.columns else 0
        )

        k4.metric(
            "คอยที่มีปัญหา",
            round(df["NC"].sum(), 2)
            if "NC" in df.columns else 0
        )

        k5, k6, k7, k8 = st.columns(4)

        k5.metric(
            "คอยพร้อมส่ง",
            round(df["Ready_To_Ship"].sum(), 2)
            if "Ready_To_Ship" in df.columns else 0
        )

        k6.metric(
            "คอยทั้งหมด",
            round(df["Total_Coil"].sum(), 2)
            if "Total_Coil" in df.columns else 0
        )

        k7.metric(
            "คอยที่เหลือ",
            round(df["Remaining_Coil"].sum(), 2)
            if "Remaining_Coil" in df.columns else 0
        )

        k8.metric(
            "Old Order",
            (
                df["Old_Order"] == "YES"
            ).sum()
            if "Old_Order" in df.columns else 0
        )

        st.divider()

        # Move KPI

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Move Coil",
            (
                df["Move_Coil_Result"] == "Move Coil"
            ).sum()
            if "Move_Coil_Result" in df.columns else 0
        )

        m2.metric(
            "Move Coil + ผลิตเพิ่ม",
            (
                df["Move_Coil_Result"] == "Move Coil + ผลิตเพิ่ม"
            ).sum()
            if "Move_Coil_Result" in df.columns else 0
        )

        m3.metric(
            "ผลิตเพิ่ม",
            (
                df["Move_Coil_Result"] == "ผลิตเพิ่ม"
            ).sum()
            if "Move_Coil_Result" in df.columns else 0
        )

        m4.metric(
            "เร่งด่วน",
            (
                df["Move_Priority"] == "HIGH"
            ).sum()
            if "Move_Priority" in df.columns else 0
        )

        st.divider()

        p1, p2, p3 = st.columns(3)

        p1.metric(
            "Move Qty",
            round(df["Move_Qty"].sum(), 2)
            if "Move_Qty" in df.columns else 0
        )

        p2.metric(
            "ต้องผลิตเพิ่ม",
            round(df["Balance_To_Produce"].sum(), 2)
            if "Balance_To_Produce" in df.columns else 0
        )

        p3.metric(
            "Move Out",
            (
                df["Move_Status"] == "Move Out"
            ).sum()
            if "Move_Status" in df.columns else 0
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
                "สถานะ",
                "จำนวน"
            ]

            st.subheader("สถานะ Move Coil")

            fig_move = px.pie(
                move_status,
                names="สถานะ",
                values="จำนวน",
                hole=0.5
            )

            st.plotly_chart(
                fig_move,
                use_container_width=True
            )

        # Aging

        if "Aging_Group" in df.columns:

            aging_df = (
                df["Aging_Group"]
                .value_counts()
                .reset_index()
            )

            aging_df.columns = [
                "อายุค้างส่ง",
                "จำนวน"
            ]

            st.subheader("อายุค้างส่ง")

            fig_aging = px.pie(
                aging_df,
                names="อายุค้างส่ง",
                values="จำนวน",
                hole=0.5
            )

            st.plotly_chart(
                fig_aging,
                use_container_width=True
            )

        # Grade

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

            st.subheader("ค้างส่งแยกตาม Grade")

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

    # ==================================================
    # BUYER
    # ==================================================

    with tab2:

        st.subheader("สรุปตาม Buyer")

        if "Buyer" in df.columns:

            buyer_df = (
                df.groupby("Buyer")
                .agg({
                    "Outstanding": "sum",
                    "Production_Add": "sum",
                    "NC": "sum",
                    "Move_Available": "sum",
                    "Move_Qty": "sum",
                    "Balance_To_Produce": "sum",
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

    # ==================================================
    # CUSTOMER
    # ==================================================

    with tab3:

        st.subheader("สรุปลูกค้า")

        if "End Cust." in df.columns:

            customer_df = (
                df.groupby("End Cust.")
                .agg({
                    "Outstanding": "sum",
                    "Production_Add": "sum",
                    "NC": "sum"
                })
                .reset_index()
            )

            st.dataframe(
                customer_df,
                use_container_width=True
            )

    # ==================================================
    # DETAIL
    # ==================================================

    with tab4:

        st.subheader("รายละเอียดข้อมูล")

        st.dataframe(
            df,
            use_container_width=True,
            height=700
        )

    # ==================================================
    # MOVE COIL
    # ==================================================

    with tab5:

        st.subheader("แนะนำ Move Coil")

        move_df = df[
            df["Move_Coil_Result"] != "CLOSED"
        ]

        cols = [
            c for c in [
                "OrderNo",
                "Buyer",
                "End Cust.",
                "SPEC_KEY",
                "Outstanding",
                "Move_Available",
                "Move_Qty",
                "Move_From_Order",
                "Move_Status",
                "Balance_To_Produce",
                "Move_Coil_Result",
                "Move_Priority"
            ]
            if c in move_df.columns
        ]

        st.dataframe(
            move_df[cols],
            use_container_width=True,
            height=700
        )

    # ==================================================
    # PLANNING
    # ==================================================

    with tab6:

        st.subheader("แผนการผลิต")

        planning_df = df[
            df["Outstanding"] > 0
        ]

        cols = [
            c for c in [
                "OrderNo",
                "Buyer",
                "SPEC_KEY",
                "Outstanding",
                "Move_Qty",
                "Balance_To_Produce",
                "Move_Priority"
            ]
            if c in planning_df.columns
        ]

        st.dataframe(
            planning_df[cols],
            use_container_width=True,
            height=700
        )

        if (
            "Move_Priority" in planning_df.columns
            and "Balance_To_Produce" in planning_df.columns
        ):

            plan_summary = (
                planning_df.groupby(
                    "Move_Priority"
                )["Balance_To_Produce"]
                .sum()
                .reset_index()
            )

            fig_plan = px.bar(
                plan_summary,
                x="Move_Priority",
                y="Balance_To_Produce",
                color="Balance_To_Produce"
            )

            st.plotly_chart(
                fig_plan,
                use_container_width=True
            )

    # ==================================================
    # MOVE FORM
    # ==================================================

    with tab7:

        st.subheader("ฟอร์ม Move Coil")

        move_form = df[
            df["Move_Coil_Result"] != "CLOSED"
        ]

        cols = [
            c for c in [
                "OrderNo",
                "Item",
                "Buyer",
                "End Cust.",
                "Prod Cd",
                "Com.SG",
                "Equi  Grade",
                "EndUse",
                "Thk",
                "Wid",
                "Move_From_Order",
                "Move_Qty",
                "Balance_To_Produce",
                "Move_Status",
                "Move_Coil_Result",
                "Move_Priority",
                "Result_After_Check",
                "Remark"
            ]
            if c in move_form.columns
        ]

        st.dataframe(
            move_form[cols],
            use_container_width=True,
            height=700
        )
