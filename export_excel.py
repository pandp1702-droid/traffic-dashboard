import pandas as pd
import numpy as np


def calculate(df):

    df = df.copy()

    if "NC COIL" in df.columns:
        df["NC"] = pd.to_numeric(
            df["NC COIL"],
            errors="coerce"
        ).fillna(0)
    else:
        df["NC"] = 0

    for col in [
        "Ord QTY+",
        "Remain Insert",
        "Slab Confirm",
        "Other+",
        "Sample+",
        "Test+",
        "P&O WP",
        "Suspend+",
        "Rdy Shp+"
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    df["Other_Suspend"] = (
        df.get("Other+", 0)
        + df.get("Suspend+", 0)
    )

    df["Sample_Test_WP_Rdy"] = (
        df.get("Sample+", 0)
        + df.get("Test+", 0)
        + df.get("P&O WP", 0)
        + df.get("Rdy Shp+", 0)
    )

    df["Remain_Insert_Slab_Confirm"] = (
        df.get("Remain Insert", 0)
        + df.get("Slab Confirm", 0)
    )

    df["Coil_Inv"] = (
        df["Other_Suspend"]
        + df["Sample_Test_WP_Rdy"]
    )

    df["Sum"] = (
        df["Remain_Insert_Slab_Confirm"]
        + df["Coil_Inv"]
    )

    if "Ord QTY+" in df.columns:
        df["Outstanding"] = (
            df["Ord QTY+"]
            - df["Sum"]
        )
    else:
        df["Outstanding"] = 0

    df["Production_Add"] = np.where(
        (df["NC"] - df["Coil_Inv"]) < 4,
        0,
        (df["NC"] - df["Coil_Inv"])
    )

    df["Remaining_Coil"] = np.maximum(
        0,
        df["Coil_Inv"] - df["NC"]
    )

    df["Move_Coil"] = df.get(
        "Rdy Shp+",
        0
    )

    df["Order_Status"] = np.where(
        df["Production_Add"] > 0,
        "OPEN",
        "CLOSED"
    )

    df["High_Risk"] = np.where(
        df["Production_Add"] > 0,
        "YES",
        "NO"
    )

    return df
