import pandas as pd
import numpy as np


def calculate(df):

    df = df.copy()

    # Create Key
    required_cols = ["Protocol", "Com.SG", "EndUse", "Thk", "Wid"]

    if all(col in df.columns for col in required_cols):
        df["KEY"] = (
            df["Protocol"].astype(str)
            + df["Com.SG"].astype(str)
            + df["EndUse"].astype(str)
            + df["Thk"].astype(str)
            + df["Wid"].astype(str)
        )

    # Temporary version
    # Avoid AK / AL / AM errors until actual columns are mapped

    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) > 0:

        df["Outstanding"] = 0
        df["Coil_Inv"] = 0
        df["Production_Add"] = 0
        df["Remain_Balance"] = 0
        df["Remain_Move"] = 0

    else:

        df["Outstanding"] = 0
        df["Coil_Inv"] = 0
        df["Production_Add"] = 0
        df["Remain_Balance"] = 0
        df["Remain_Move"] = 0

    df["Order_Status"] = "OPEN"

    return df
