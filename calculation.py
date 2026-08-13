import pandas as pd
import numpy as np


def calculate(df):

    df = df.copy()

    # =====================================
    # CONVERT NUMERIC COLUMNS
    # =====================================

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

    # =====================================
    # OUTSTANDING
    # =====================================

    if "Need" in df.columns:

        df["Outstanding"] = df["Need"]

    else:

        df["Outstanding"] = 0

    # =====================================
    # COIL INVENTORY
    # =====================================

    inventory_columns = [
        "Other+",
        "Sample+",
        "Test+",
        "P&O WP",
        "OSP+",
        "Suspend+",
        "Rdy Shp+"
    ]

    available_inventory = [
        col
        for col in inventory_columns
        if col in df.columns
    ]

    if available_inventory:

        df["Coil_Inv"] = (
            df[available_inventory]
            .sum(axis=1)
        )

    else:

        df["Coil_Inv"] = 0

    # =====================================
    # PRODUCTION ADD
    # =====================================

    df["Production_Add"] = np.maximum(
        0,
        df["Outstanding"]
        - df["Coil_Inv"]
    )

    # =====================================
    # REMAINING COIL
    # =====================================

    df["Remaining_Coil"] = np.maximum(
        0,
        df["Coil_Inv"]
        - df["Outstanding"]
    )

    # =====================================
    # MOVE COIL
    # =====================================

    if "Rdy Shp+" in df.columns:

        df["Move_Coil"] = df["Rdy Shp+"]

    else:

        df["Move_Coil"] = 0

    # =====================================
    # INVENTORY COVERAGE %
    # =====================================

    if (
        "Outstanding" in df.columns
        and "Coil_Inv" in df.columns
    ):

        df["Inventory_Coverage_Pct"] = np.where(
            df["Outstanding"] > 0,
            (
                df["Coil_Inv"]
                / df["Outstanding"]
            ) * 100,
            0
        )

    else:

        df["Inventory_Coverage_Pct"] = 0

    # =====================================
    #
