import pandas as pd
import numpy as np


def calculate(df):

    df = df.copy()

    # Convert numeric columns
    cols = [
        "Remain Insert",
        "Slab Confirm",
        "Need",
        "Other+",
        "Sample+",
        "Test+",
        "P&O WP",
        "OSP+",
        "Suspend+",
        "Rdy Shp+"
    ]

    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    # Outstanding
    if "Need" in df.columns:
        df["Outstanding"] = df["Need"]
    else:
        df["Outstanding"] = 0

    # Coil Inventory
    inventory_cols = [
        "Other+",
        "Sample+",
        "Test+",
        "P&O WP",
        "OSP+",
        "Suspend+",
        "Rdy Shp+"
    ]

    available = [
        col
        for col in inventory_cols
        if col in df.columns
    ]

    if available:
        df["Coil_Inv"] = df[available].sum(axis=1)
    else:
        df["Coil_Inv"] = 0

    # Production Add
    df["Production_Add"] = np.where(
        (df["Outstanding"] - df["Coil_Inv"]) < 0,
        0,
        df["Outstanding"] - df["Coil_Inv"]
    )

    # Move Coil
    if "Rdy Shp+" in df.columns:
        df["Move_Coil"] = df["Rdy Shp+"]
    else:
        df["Move_Coil"] = 0

    # Order Status
    df["Order_Status"] = np.where(
        df["Production_Add"] > 0,
        "OPEN",
        "CLOSED"
    )

    return df
