import io
import pandas as pd


def export_to_excel(df):

    output = io.BytesIO()

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    summary = pd.DataFrame({

        "Metric": [

            "Outstanding",
            "Coil Inventory",
            "Production Add",
            "Remaining Coil",
            "Move Available",
            "NC",
            "Open Orders",
            "Closed Orders",
            "Total Orders",
            "Total Buyers",
            "Total Customers"

        ],

        "Value": [

            df["Outstanding"].sum()
            if "Outstanding" in df.columns
            else 0,

            df["Coil_Inv"].sum()
            if "Coil_Inv" in df.columns
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

            df["NC"].sum()
            if "NC" in df.columns
            else 0,

            (
                df["Close_Order"] == "Failed"
            ).sum()
            if "Close_Order" in df.columns
            else 0,

            (
                df["Close_Order"] == "ปิด"
            ).sum()
            if "Close_Order" in df.columns
            else 0,

            len(df),

            df["Buyer"].nunique()
            if "Buyer" in df.columns
            else 0,

            df["End Cust."].nunique()
            if "End Cust." in df.columns
            else 0

        ]

    })

    # =====================================
    # BUYER SUMMARY
    # =====================================

    buyer_summary = pd.DataFrame()

    if (
        "Buyer" in df.columns
        and "Outstanding" in df.columns
    ):

        buyer_summary = (
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

    # =====================================
    # CUSTOMER SUMMARY
    # =====================================

    customer_summary = pd.DataFrame()

    if (
        "End Cust." in df.columns
        and "Outstanding" in df.columns
    ):

        customer_summary = (
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

    # =====================================
    # MOVE STATUS
    # =====================================

    move_status = pd.DataFrame()

    if "Move_Coil_Result" in df.columns:

        move_status = (
            df["Move_Coil_Result"]
            .value_counts()
            .reset_index()
        )

        move_status.columns = [
            "Move Status",
            "Count"
        ]

    # =====================================
    # HIGH RISK
    # =====================================

    risk_df = pd.DataFrame()

    if "High_Risk" in df.columns:

        risk_df = df[
            df["High_Risk"] == "YES"
        ]

    # =====================================
    # EXPORT
    # =====================================

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        summary.to_excel(
            writer,
            sheet_name="Executive Summary",
            index=False
        )

        df.to_excel(
            writer,
            sheet_name="Data",
            index=False
        )

        if not buyer_summary.empty:

            buyer_summary.to_excel(
                writer,
                sheet_name="Buyer Summary",
                index=False
            )

        if not customer_summary.empty:

            customer_summary.to_excel(
                writer,
                sheet_name="Customer Summary",
                index=False
            )

        if not move_status.empty:

            move_status.to_excel(
                writer,
                sheet_name="Move Status",
                index=False
            )

        if not risk_df.empty:

            risk_df.to_excel(
                writer,
                sheet_name="High Risk Orders",
                index=False
            )

    output.seek(0)

    return output
