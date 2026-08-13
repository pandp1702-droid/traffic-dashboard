import pandas as pd
import numpy as np


def calculate(df):

    df = df.copy()

    # NC
    if "NC COIL" in df.columns:
        df["NC"] = pd.to_numeric(
            df["NC COIL"],
            errors="coerce"
        ).fillna(0)
    else:
        df["NC"] = 0

    # Convert columns
    numeric_cols = [
        "Ord QTY+",
        "Remain Insert",
        "Slab Confirm",
        "Other+",
        "Sample+",
        "Test+",
        "P&O WP",
        "Suspend+",
        "Rdy Shp+"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    # Spec Key
    required = [
        "Com.SG",
        "Equi  Grade",
        "EndUse",
        "Thk",
        "Cert. Cust."
    ]

    if all(col in df.columns for col in required):
        df["SPEC_KEY"] = (
            df["Com.SG"].astype(str)
            + df["Equi  Grade"].astype(str)
            + df["EndUse"].astype(str)
            + df["Thk"].astype(str)
            + df["Cert. Cust."].astype(str)
        )
    else:
        df["SPEC_KEY"] = ""

    # Other + Suspend
    df["Other_Suspend"] = (
        df.get("Other+", 0)
        + df.get("Suspend+", 0)
    )

    # Remain Insert + Slab Confirm
    df["Remain_Insert_Slab_Confirm"] = (
        df.get("Remain Insert", 0)
        + df.get("Slab Confirm", 0)
    )

    # Sample + Test + PO WP + Ready Ship
    df["Sample_Test_WP_Rdy"] = (
        df.get("Sample+", 0)
        + df.get("Test+", 0)
        + df.get("P&O WP", 0)
        + df.get("Rdy Shp+", 0)
    )

    # Coil Inventory
    df["Coil_Inv"] = (
        df["Other_Suspend"]
        + df["Sample_Test_WP_Rdy"]
    )

    # Sum
    df["Sum"] = (
        df["Remain_Insert_Slab_Confirm"]
        + df["Coil_Inv"]
    )

    # Outstanding
    if "Ord QTY+" in df.columns:
        df["Outstanding"] = (
            df["Ord QTY+"]
            - df["Sum"]
        )
    else:
        df["Outstanding"] = 0

    # Production Add
    df["Production_Add"] = np.where(
        (df["NC"] - df["Coil_Inv"]) < 4,
        0,
        (df["NC"] - df["Coil_Inv"])
    )

    # Remaining Coil
    remaining = np.where(
        df["NC"] > 3.999,
        df["Coil_Inv"] - df["NC"],
        df["Coil_Inv"]
    )

    remaining = np.maximum(0, remaining)

    df["Remaining_Coil"] = np.where(
        remaining < 4,
        0,
        remaining
    )

    # Move Available
    df["Move_Available"] = (
        df.get("Sample+", 0)
        + df.get("Test+", 0)
        + df.get("P&O WP", 0)
        + df.get("Rdy Shp+", 0)
    )

    # Move Coil Result
    df["Move_Coil_Result"] = np.where(
        df["Outstanding"] <= 0,
        "",
        np.where(
            df["Move_Available"] >= df["Outstanding"],
            "MOVE COIL",
            np.where(
                df["Move_Available"] > 0,
                "MOVE COIL + PRODUCE",
                "WAITING MOVE"
            )
        )
    )

    df["Move_Coil"] = df["Move_Available"]

    # Order Status
    df["Order_Status"] = np.where(
        df["Production_Add"] > 0,
        "OPEN",
        "CLOSED"
    )

    # Close Order
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

    # High Risk
    df["High_Risk"] = np.where(
        df["Production_Add"] > 0,
        "YES",
        "NO"
    )

    return df
