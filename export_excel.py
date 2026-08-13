import io
import pandas as pd


def export_to_excel(df):

    output = io.BytesIO()

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    summary = pd.DataFrame({

        "Metric": [

            "Orders",
            "Outstanding",
            "Not Produced",
            "In Production",
            "Ready To Ship",
            "Total Coil",
            "NC Coil",
            "Production Add",
            "Remaining Coil",
            "Move Available",
            "Old Orders"

        ],

        "Value": [

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
                "Ready_To_Ship": "sum"
            })
            .reset_index()
            .sort_values(
                "Outstanding",
                ascending=False
            )
        )

    # =====================================
    # CUSTOMER
