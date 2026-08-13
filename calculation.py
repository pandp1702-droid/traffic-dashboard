import pandas as pd
import numpy as np


def calculate(df):

    df = df.copy()

    numeric_columns = [
        "Need",
        "Remain Insert",
        "Slab Confirm",
        "Other+",
        "Sample+",
        "Test+",
        "P&O WP",
        "OSP+",
        "Suspend+",
        "Rdy Shp+"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    # Outstanding
    df["Outstanding"] = (
        df["Need"]
        if "Need" in df.columns
        else 0
    )

    # Coil Inventory
    inventory_columns = [
        "Other+",
        "Sample+",
        "Test+",
        "P&O WP",
        "OSP+",
        "Suspend+",
        "Rdy Shp+"
    ]

    existing_inventory = [
        col
        for col in inventory_columns
        if col in df.columns
    ]

    if existing_inventory:
        df["Coil_Inv"] = df[existing_inventory].sum(axis=1)
    else:
        df["Coil_Inv"] = 0

    # Production Add
    df["Production_Add"] = np.maximum(
        0,
        df["Outstanding"] - df["Coil_Inv"]
    )

    # Remaining Coil
    df["Remaining_Coil"] = np.maximum(
        0,
        df["Coil_Inv"] - df["Outstanding"]
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

    # Order Item Key
    if (
        "OrderNo" in df.columns
        and "Item" in df.columns
    ):
        df["Order_Item_Key"] = (
            df["OrderNo"].astype(str)
            + "_"
            + df["Item"].astype(str)
        )

    # Buyer Customer Key
    if (
        "Buyer" in df.columns
        and "End Cust." in df.columns
    ):
        df["Buyer_Customer"] = (
            df["Buyer"].astype(str)
            + "_"
            + df["End Cust."].astype(str)
        )
