import io
import pandas as pd


def export_to_excel(df):

    output = io.BytesIO()

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    executive_summary = pd.DataFrame({
        "รายการ": [
            "จำนวนออร์เดอร์",
            "ค้างส่ง",
            "คอยยังไม่ผลิต",
            "คอยอยู่ระหว่างผลิต",
            "คอยพร้อมส่ง",
            "คอยทั้งหมด",
            "คอยที่มีปัญหา",
            "ผลิตเพิ่ม",
            "คอยที่เหลือ",
            "คอย Move ได้",
            "Move Qty",
            "ต้องผลิตเพิ่ม",
            "Old Order"
        ],
        "ค่า": [
            len(df),

            df["Outstanding"].sum()
            if "Outstanding" in df.columns
            else 0,

            df["Not_Produced"].sum()
            if "Not_Produced" in df.columns
            else 0,

            df["In_Production"].sum()
            if "In_Production" in df.columns
            else 0,

            df["Ready_To_Ship"].sum()
            if "Ready_To_Ship" in df.columns
            else 0,

            df["Total_Coil"].sum()
            if "Total_Coil" in df.columns
            else 0,

            df["NC"].sum()
            if "NC" in df.columns
            else 0,

            df["Production_Add"].sum()
            if "Production_Add" in df.columns
            else 0,

            df["Remaining_Coil"].sum()
            if "Remaining_Coil" in df.columns
            else 0,

            df["Move_Available"].sum()
            if "Move_Available" in df.columns
            else 0,

            df["Move_Qty"].sum()
            if "Move_Qty" in df.columns
            else 0,

            df["Balance_To_Produce"].sum()
            if "Balance_To_Produce" in df.columns
            else 0,

            (
                df["Old_Order"] == "YES"
            ).sum()
            if "Old_Order" in df.columns
            else 0
        ]
    })

    # =====================================
    # BUYER SCORECARD
    # =====================================

    buyer_scorecard = pd.DataFrame()

    if "Buyer" in df.columns:

        buyer_scorecard = (
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

        buyer_scorecard.columns = [
            "Buyer",
            "ค้างส่ง",
            "ผลิตเพิ่ม",
            "NC",
            "คอย Move ได้",
            "Move Qty",
            "ต้องผลิตเพิ่ม",
            "คอยพร้อมส่ง"
        ]

    # =====================================
    # CUSTOMER SUMMARY
    # =====================================

    customer_summary = pd.DataFrame()

    if "End Cust." in df.columns:

        customer_summary = (
            df.groupby("End Cust.")
            .agg({
                "Outstanding": "sum",
                "Production_Add": "sum",
                "NC": "sum",
                "Move_Available": "sum"
            })
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
        )

    # =====================================
    # GRADE SUMMARY
    # =====================================

    grade_summary = pd.DataFrame()

    if "Com.SG" in df.columns:

        grade_summary = (
            df.groupby("Com.SG")
            .agg({
                "Outstanding": "sum",
                "Production_Add": "sum"
            })
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
        )

    # =====================================
    # MOVE COIL STATUS
    # =====================================

    move_status = pd.DataFrame()

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

    # =====================================
    # MOVE RECOMMENDATION
    # =====================================

    move_recommendation = pd.DataFrame()

    if "Move_Coil_Result" in df.columns:

        move_recommendation = (
            df[
                df["Move_Coil_Result"]
                != "CLOSED"
            ]
        )

    # =====================================
    # PRODUCTION PLANNING
    # =====================================

    planning_df = pd.DataFrame()

    if "Outstanding" in df.columns:

        planning_df = (
            df[
                df["Outstanding"] > 0
            ]
        )

    # =====================================
    # HIGH RISK
    # =====================================

    high_risk_df = pd.DataFrame()

    if "High_Risk" in df.columns:

        high_risk_df = (
            df[
                df["High_Risk"] == "YES"
            ]
        )

    # =====================================
    # OLD ORDERS
    # =====================================

    old_order_df = pd.DataFrame()

    if "Old_Order" in df.columns:

        old_order_df = (
            df[
                df["Old_Order"] == "YES"
            ]
        )

    # =====================================
    # AGING SUMMARY
    # =====================================

    aging_summary = pd.DataFrame()

    if "Aging_Group" in df.columns:

        aging_summary = (
            df["Aging_Group"]
            .value_counts()
            .reset_index()
        )

        aging_summary.columns = [
            "อายุค้างส่ง",
            "จำนวน"
        ]

    # =====================================
    # EXPORT
    # =====================================

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        executive_summary.to_excel(
            writer,
            sheet_name="สรุปผู้บริหาร",
            index=False
        )

        df.to_excel(
            writer,
            sheet_name="Data",
            index=False
        )

        if not buyer_scorecard.empty:
            buyer_scorecard.to_excel(
                writer,
                sheet_name="สรุป Buyer",
                index=False
            )

        if not customer_summary.empty:
            customer_summary.to_excel(
                writer,
                sheet_name="สรุปลูกค้า",
                index=False
            )

        if not grade_summary.empty:
            grade_summary.to_excel(
                writer,
                sheet_name="สรุป Grade",
                index=False
            )

        if not move_status.empty:
            move_status.to_excel(
                writer,
                sheet_name="สถานะ Move Coil",
                index=False
            )

        if not move_recommendation.empty:
            move_recommendation.to_excel(
                writer,
                sheet_name="แนะนำ Move Coil",
                index=False
            )

        if not planning_df.empty:
            planning_df.to_excel(
                writer,
                sheet_name="แผนการผลิต",
                index=False
            )

        if not high_risk_df.empty:
            high_risk_df.to_excel(
                writer,
                sheet_name="High Risk Orders",
                index=False
            )

        if not old_order_df.empty:
            old_order_df.to_excel(
                writer,
                sheet_name="Old Orders",
                index=False
            )

        if not aging_summary.empty:
            aging_summary.to_excel(
                writer,
                sheet_name="Aging Summary",
                index=False
            )

    output.seek(0)

    return output.getvalue()
