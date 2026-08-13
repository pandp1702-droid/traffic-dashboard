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

    if "NC COIL" in df.columns:
        df["NC"] = df["NC COIL"]
    else:
        df["NC"] = 0

    # =====================================
    # SPEC KEY
    # = I + J + K + L + N
    # =====================================

    key_cols = [
        "Com.SG",
        "Equi  Grade",
        "EndUse",
        "Thk",
        "Cert. Cust."
    ]

    if all(col in df.columns for col in key_cols):

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
    # Other + Suspend
    # =====================================

    df["Other_Suspend"] = (
        df.get("Other+", 0)
        + df.get("Suspend+", 0)
    )

    # =====================================
    # Remain Insert + Slab Confirm
    # =====================================

    df["Remain_Insert_Slab_Confirm"] = (
        df.get("Remain Insert", 0)
        + df.get("Slab Confirm", 0)
    )

    # =====================================
    # Sample + Test + P&O WP + Ready Ship
    # =====================================

    df["Sample_Test_WP_Rdy"] = (
        df.get("Sample+", 0)
        + df.get("Test+", 0)
        + df.get("P&O WP", 0)
        + df.get("Rdy Shp+", 0)
    )

    # =====================================
    # Coil Inv
    # =====================================

    df["Coil_Inv"] = (
        df["Other_Suspend"]
        + df["Sample_Test_WP_Rdy"]
    )

    # =====================================
    # Sum
    # =====================================

    df["Sum"] = (
        df["Remain_Insert_Slab_Confirm"]
        + df["Coil_Inv"]
    )

    # =====================================
    # Outstanding
    # Ord QTY - Sum
    # =====================================

    if "Ord QTY+" in df.columns:

        df["Outstanding"] = (
            df["Ord QTY+"]
            - df["Sum"]
        )

    else:

        df["Outstanding"] = 0

    # =====================================
    # Production Add
    # =IF((NC-CoilInv)<4,0,(NC-CoilInv))
    # =====================================

    df["Production_Add"] = np.where(
        (df["NC"] - df["Coil_Inv"]) < 4,
        0,
        (df["NC"] - df["Coil_Inv"])
    )

    # =====================================
    # Remaining Coil
    # =====================================

    remaining = np.where(

        df["NC"] > 3.999,

        df["Coil_Inv"] - df["NC"],

        df["Coil_Inv"]

    )

    remaining = np.maximum(
        0,
        remaining
    )

    df["Remaining_Coil"] = np.where(
        remaining < 4,
        0,
        remaining
    )

    # =====================================
    # Remaining Coil + Move
    # =====================================

    move_value = np.where(

        df["NC"] <= 3.999,

        df["Remaining_Coil"],

        np.where(

            df["NC"] <= df["Outstanding"],

            df["Remaining_Coil"],

            np.maximum(
                0,
                df["Remaining_Coil"]
                - (
                    df["NC"]
                    - df["Outstanding"]
                )
            )
        )
    )

    df["Remaining_Coil_Move"] = np.where(
        move_value < 4,
        0,
        move_value
    )

    # =====================================
    # Order+
    # =====================================

    df["Order_Plus"] = np.where(
        df["Production_Add"] > 3.999,
        "YES",
        "NO"
    )

    # =====================================
    # Close Order
    # =====================================

    df["Close_Order"] = np.where(
        (
            df["Production_Add"] < 3.999
        )
        &
        (
            df["Sum"] == 0
        ),
        "ปิด",
        "Failed"
    )

    # =====================================
    # Move Available
    # ใช้เฉพาะ Coil พร้อม Move
    # =====================================

    df["Move_Available"] = (
        df.get("Sample+", 0)
        + df.get("Test+", 0)
        + df.get("P&O WP", 0)
        + df.get("Rdy Shp+", 0)
    )

    # =====================================
    # Move Coil Result
    # =====================================

    df["Move_Coil_Result"] = np.where(

        df["Outstanding"] <= 0,

        "",

        np.where(

            df["Move_Available"]
            >= df["Outstanding"],

            "MOVE COIL",

            np.where(

                df["Move_Available"] > 0,

                "MOVE COIL + PRODUCE",

                "WAITING MOVE"
            )
        )
    )

    # =====================================
    # Inventory Coverage %
    # =====================================

    df["Inventory_Coverage_Pct"] = np.where(
        df["Outstanding"] > 0,
        (
            df["Coil_Inv"]
            / df["Outstanding"]
        ) * 100,
        0
    )

    # =====================================
    # High Risk
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
    # Old Order
    # =====================================

    if "Last Shipment Date" in df.columns:

        shipment_date = pd.to_datetime(
            df["Last Shipment Date"],
            errors="coerce"
        )

        df["Old_Order"] = np.where(
            (
                pd.Timestamp.today()
                - shipment_date
            ).dt.days > 90,
            "YES",
            "NO"
        )

    else:

        df["Old_Order"] = "NO"

    return df
