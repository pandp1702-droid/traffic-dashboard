import pandas as pd
import numpy as np


def calculate(df):

    df = df.copy()

    # =====================================
    # CONVERT NUMERIC
    # =====================================

    numeric_columns = [
        "Ord QTY+",
        "Remain Insert",
        "Slab Confirm",
        "Other+",
        "Sample+",
        "Test+",
        "P&O WP",
        "OSP+",
        "Suspend+",
        "Rdy Shp+",
        "NC COIL"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    # =====================================
    # NC
    # =====================================

    df["NC"] = (
        df["NC COIL"]
        if "NC COIL" in df.columns
        else 0
    )

    # =====================================
    # SPEC KEY
    # =====================================

    required_cols = [
        "Com.SG",
        "Equi  Grade",
        "EndUse",
        "Thk",
        "Cert. Cust."
    ]

    if all(col in df.columns for col in required_cols):

        df["SPEC_KEY"] = (
            df["Com.SG"].astype(str)
            + df["Equi  Grade"].astype(str)
            + df["EndUse"].astype(str)
            + df["Thk"].astype(str)
            + df["Cert. Cust."].astype(str)
        )

    else:

        df["SPEC_KEY"] = ""

    # =====================================
    # GROUP CALCULATION
    # =====================================

    df["Other_Suspend"] = (
        df.get("Other+", 0)
        + df.get("Suspend+", 0)
    )

    df["Remain_Insert_Slab_Confirm"] = (
        df.get("Remain Insert", 0)
        + df.get("Slab Confirm", 0)
    )

    df["Sample_Test_WP_Rdy"] = (
        df.get("Sample+", 0)
        + df.get("Test+", 0)
        + df.get("P&O WP", 0)
        + df.get("Rdy Shp+", 0)
    )

    # =====================================
    # COIL INVENTORY
    # =====================================

    df["Coil_Inv"] = (
        df["Other_Suspend"]
        + df["Sample_Test_WP_Rdy"]
    )

    # =====================================
    # SUM
    # =====================================

    df["Sum"] = (
        df["Remain_Insert_Slab_Confirm"]
        + df["Coil_Inv"]
    )

    # =====================================
    # OUTSTANDING
    # =====================================

    if "Ord QTY+" in df.columns:

        df["Outstanding"] = (
            df["Ord QTY+"]
            - df["Sum"]
        )

    else:

        df["Outstanding"] = 0

    # =====================================
    # PRODUCTION ADD
    # =====================================

    df["Production_Add"] = np.where(
        (df["NC"] - df["Coil_Inv"]) < 4,
        0,
        (df["NC"] - df["Coil_Inv"])
    )

    # =====================================
    # REMAINING COIL
    # =====================================

    remaining = np.where(
        df["NC"] > 3.999,
        df["Coil_Inv"] - df["NC"],
        df["Coil_Inv"]
    )

    remaining = np.maximum(
        remaining,
        0
    )

    df["Remaining_Coil"] = np.where(
        remaining < 4,
        0,
        remaining
    )

    # =====================================
    # MOVE AVAILABLE
    # =====================================

    df["Move_Available"] = (
        df.get("Sample+", 0)
        + df.get("Test+", 0)
        + df.get("P&O WP", 0)
        + df.get("Rdy Shp+", 0)
    )

    # =====================================
    # MOVE COIL RESULT
    # =====================================

    df["Move_Coil_Result"] = np.where(
        df["Outstanding"] <= 0,
        "CLOSED",
        np.where(
            df["Move_Available"] >= df["Outstanding"],
            "MOVE COIL",
            np.where(
                df["Move_Available"] > 0,
                "MOVE + PRODUCE",
                "PRODUCE ONLY"
            )
        )
    )

    # =====================================
    # MOVE PRIORITY
    # =====================================

    df["Move_Priority"] = np.select(
        [
            df["Outstanding"] >= 50,
            df["Outstanding"] >= 20,
            df["Outstanding"] > 0
        ],
        [
            "HIGH",
            "MEDIUM",
            "LOW"
        ],
        default=""
    )

    # =====================================
    # TEMP MOVE MATCH
    # =====================================

    df["Move_From_Order"] = ""
    df["Move_Qty"] = 0.0

    # =====================================
    # ORDER STATUS
    # =====================================

    df["Order_Plus"] = np.where(
        df["Production_Add"] > 3.999,
        "YES",
        "NO"
    )

    df["Close_Order"] = np.where(
        (
            df["Production_Add"] < 3.999
        )
        & (
            df["Sum"] == 0
        ),
        "ปิด",
        "Failed"
    )

    # =====================================
    # INVENTORY COVERAGE
    # =====================================

    df["Inventory_Coverage_Pct"] = np.where(
        df["Outstanding"] > 0,
        (
            df["Coil_Inv"]
            /
            df["Outstanding"]
        ) * 100,
        0
    )

    # =====================================
    # HIGH RISK
    # =====================================

    df["High_Risk"] = np.where(
        df["Production_Add"] > 0,
        "YES",
        "NO"
    )

    # =====================================
    # SSI KPI
    # =====================================

    df["Not_Produced"] = (
        df["Remain_Insert_Slab_Confirm"]
    )

    df["In_Production"] = (
        df["Other_Suspend"]
    )

    df["Ready_To_Ship"] = (
        df["Sample_Test_WP_Rdy"]
    )

    df["Problem_Coil"] = (
        df["NC"]
    )

    df["Total_Coil"] = (
        df["Not_Produced"]
        + df["In_Production"]
        + df["Ready_To_Ship"]
    )

    # =====================================
    # DATE / AGING
    # =====================================

    if "Last Shipment Date" in df.columns:

        shipment_date = pd.to_datetime(
            df["Last Shipment Date"].astype(str),
            format="%Y%m%d",
            errors="coerce"
        )

        aging_days = (
            pd.Timestamp.today()
            - shipment_date
        ).dt.days

        df["Old_Order"] = np.where(
            aging_days > 90,
            "YES",
            "NO"
        )

        df["Shipment_Month"] = (
            shipment_date.dt.strftime("%Y-%m")
        )

        df["Aging_Group"] = np.select(
            [
                aging_days <= 30,
                aging_days <= 60,
                aging_days <= 90,
                aging_days > 90
            ],
            [
                "0-30 Days",
                "31-60 Days",
                "61-90 Days",
                "90+ Days"
            ],
            default="Unknown"
        )

    else:

        df["Old_Order"] = "NO"
        df["Shipment_Month"] = ""
        df["Aging_Group"] = ""

    return df
