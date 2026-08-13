import pandas as pd
import numpy as np

def calculate(df):
    df = df.copy()

    # XXX Key
    df["XXX"] = (
        df["Protocol"].astype(str) +
        df["Com.SG"].astype(str) +
        df["EndUse"].astype(str) +
        df["Thk"].astype(str) +
        df["Wid"].astype(str)
    )

    df["Coil inv"] = df["AK"] + df["AL"] + df["AM"] + df["AN"] + df["AO"] + df["AS"]
    df["Other+Suspend+"] = df["AP"] + df["AV"]
    df["Remain Insert+Slab Confirm"] = df["AH"] + df["AI"]
    df["Sample+Test+PO WP+Rdy Shp"] = df["AQ"] + df["AR"] + df["AT"] + df["AW"]

    df["Sum"] = (
        df["Coil inv"] +
        df["Other+Suspend+"] +
        df["Remain Insert+Slab Confirm"] +
        df["Sample+Test+PO WP+Rdy Shp"]
    )

    df["Outstanding"] = df["AF"] - df["BC"] - df["BA"]

    df["ผลิตเพิ่ม"] = np.where(
        (df["Outstanding"] - df["Sum"]) < 4,
        0,
        df["Outstanding"] - df["Sum"]
    )

    def remain(row):
        value = row["Sum"] - row["Outstanding"] if row["Outstanding"] > 3.999 else row["Sum"]
        value = max(0, value)
        return 0 if value < 4 else value

    df["คอยที่เหลือ"] = df.apply(remain, axis=1)

    def move(row):
        if row["Outstanding"] <= 3.999:
            value = row["Sample+Test+PO WP+Rdy Shp"]
        elif row["Outstanding"] <= row["Coil inv"]:
            value = row["Sample+Test+PO WP+Rdy Shp"]
        else:
            value = max(0, row["Sample+Test+PO WP+Rdy Shp"] - (row["Outstanding"] - row["Coil inv"]))

        return 0 if value < 4 else value

    df["คอยที่เหลือ พร้อม Move"] = df.apply(move, axis=1)

    df["NC"] = df["CF"]

    df["ปิดOrder"] = np.where(
        ((df["ผลิตเพิ่ม"] < 3.999) & (df["Sum"] == 0)),
        "ปิด",
        "Failed"
    )

    df["Order+"] = np.where(df["ผลิตเพิ่ม"] > 3.999, "YES", "NO")

    return df
