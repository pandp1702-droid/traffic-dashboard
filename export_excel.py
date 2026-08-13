import io
import pandas as pd


def export_to_excel(df):

    output = io.BytesIO()

    # =====================================
    # KPI CALCULATION
    # =====================================

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

    remaining_coil = (
        df["Remaining_Coil"].sum()
        if "Remaining_Coil" in df.columns
        else 0
    )

    move_coil = (
        df["Move_Coil"].sum()
        if "Move_Coil" in df.columns
        else 0
    )

    total_orders = len(df)

    total_buyers = (
        df["Buyer"].nunique()
        if "Buyer" in df.columns
        else 0
    )

    total_customers = (
        df["End Cust."].nunique()
        if "End Cust." in df.columns
        else 0
    )

    open_orders = (
        (df["Order_Status"] == "OPEN").sum()
        if "Order_Status" in df.columns
        else 0
    )

    closed_orders = (
        (df["Order_Status"] == "CLOSED").sum()
        if "Order_Status" in df.columns
        else 0
    )

    avg_outstanding = (
        round(
            df["Outstanding"].mean(),
            2
        )
        if "Outstanding" in df.columns
        else 0
    )

    coverage = 0

    if (
        "Outstanding" in df.columns
        and "Coil_Inv" in df.columns
        and outstanding > 0
    ):
        coverage = round(
            (coil_inv / outstanding) * 100,
            2
        )

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    executive_summary = pd.DataFrame({

        "Metric": [

            "Outstanding",
            "Coil Inventory",
            "Production Add",
            "Remaining Coil",
            "Move Coil",
            "Total Orders",
            "Total Buyers",
            "Total Customers",
            "Open Orders",
            "Closed Orders",
            "Average Outstanding",
            "Inventory Coverage %"

        ],

        "Value": [

            outstanding,
            coil_inv,
            production_add,
            remaining_coil,
            move_coil,
            total_orders,
            total_buyers,
            total_customers,
            open_orders,
            closed_orders,
            avg_outstanding,
            coverage

        ]
    })

    # =====================================
    # VALIDATION SUMMARY
    # =====================================

    validation_summary = pd.DataFrame({

        "Check": [

            "Total Rows",
            "Total Buyers",
            "Total Customers",
            "Open Orders",
            "Closed Orders"

        ],

        "Value": [

            total_orders,
            total_buyers,
            total_customers,
            open_orders,
            closed_orders

        ]
    })

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # Executive Summary
        executive_summary.to_excel(
            writer,
            sheet_name="Executive Summary",
            index=False
        )

        # Validation
        validation_summary.to_excel(
            writer,
            sheet_name="Validation",
            index=False
        )

        # Raw Data
        df.to_excel(
            writer,
            sheet_name="Data",
            index=False
        )

        # Buyer Summary
        if (
            "Buyer" in df.columns
            and "Outstanding" in df.columns
        ):

            buyer_summary = (
                df.groupby("Buyer")["Outstanding"]
                .sum()
                .reset_index()
                .sort_values(
                    "Outstanding",
                    ascending=False
                )
            )

            buyer_summary.to_excel(
                writer,
                sheet_name="Buyer Summary",
                index=False
            )

        # Customer Summary
        if (
            "End Cust." in df.columns
            and "Outstanding" in df.columns
        ):

            customer_summary = (
                df.groupby("End Cust.")["Outstanding"]
                .sum()
                .reset_index()
                .sort_values(
                    "Outstanding",
                    ascending=False
                )
            )

            customer_summary.to_excel(
                writer,
                sheet_name="Customer Summary",
                index=False
            )

        # Grade Summary
        if (
            "Com.SG" in df.columns
            and "Outstanding" in df.columns
        ):

            grade_summary = (
                df.groupby("Com.SG")["Outstanding"]
                .sum()
                .reset_index()
                .sort_values(
                    "Outstanding",
                    ascending=False
                )
            )

            grade_summary.to_excel(
                writer,
                sheet_name="Grade Summary",
                index=False
            )

        # Width Summary
        if (
            "Wid" in df.columns
            and "Outstanding" in df.columns
        ):

            width_summary = (
                df.groupby("Wid")["Outstanding"]
                .sum()
                .reset_index()
                .sort_values(
                    "Outstanding",
                    ascending=False
                )
            )

            width_summary.to_excel(
                writer,
                sheet_name="Width Summary",
                index=False
            )

        # Protocol Summary
        if (
            "Protocol" in df.columns
            and "Outstanding" in df.columns
        ):

            protocol_summary = (
                df.groupby("Protocol")["Outstanding"]
                .sum()
                .reset_index()
                .sort_values(
                    "Outstanding",
                    ascending=False
                )
            )

            protocol_summary.to_excel(
                writer,
                sheet_name="Protocol Summary",
                index=False
            )

        # High Risk Orders
        if "Production_Add" in df.columns:

            risk_df = df[
                df["Production_Add"] > 0
            ]

            risk_df.to_excel(
                writer,
                sheet_name="High Risk Orders",
                index=False
            )

    output.seek(0)

    return output
