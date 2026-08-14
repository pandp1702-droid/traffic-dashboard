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
    # OTHER + SUSPEND
    # =====================================

    df["Other_Suspend"] = (
        df.get("Other+", 0)
        + df.get("Suspend+", 0)
    )

    # =====================================
    # REMAIN INSERT + SLAB CONFIRM
    # =====================================

    df["Remain_Insert_Slab_Confirm"] = (
        df.get("Remain Insert", 0)
        + df.get("Slab Confirm", 0)
    )

    # =====================================
    # SAMPLE + TEST + PO WP + RDY SHP
    # =====================================

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
        0,
        remaining
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
    # MOVE RESULT
    # =====================================

    df["Move_Coil_Result"] = np.where(
        df["Outstanding"] <= 0,
        "CLOSED",
        np.where(
            df["Move_Available"] >= df["Outstanding"],
            "Move Coil",
            np.where(
                df["Move_Available"] > 0,
                "Move Coil + ผลิตเพิ่ม",
                "ผลิตเพิ่ม"
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
    # MOVE PLANNING
    # =====================================

    df["Move_Qty"] = np.minimum(
        df["Outstanding"],
        df["Move_Available"]
    )

    df["Move_Qty"] = np.maximum(
        0,
        df["Move_Qty"]
    )

    df["Balance_To_Produce"] = np.maximum(
        0,
        df["Outstanding"]
        - df["Move_Qty"]
    )

    df["Move_From_Order"] = ""

    # =====================================
    # RESULT AFTER CHECK
    # =====================================

    df["Result_After_Check"] = np.where(
        df["Move_Coil_Result"] == "Move Coil",
        "ผ่าน",
        np.where(
            df["Move_Coil_Result"] == "Move Coil + ผลิตเพิ่ม",
            "ผ่านบางส่วน",
            "ต้องผลิตเพิ่ม"
        )
    )

    # =====================================
    # REMARK
    # =====================================

    df["Remark"] = np.where(
        df["Move_Coil_Result"] == "Move Coil",
        "Move Available",
        np.where(
            df["Move_Coil_Result"] == "Move Coil + ผลิตเพิ่ม",
            "Move Available แต่ต้องผลิตเพิ่ม",
            "ไม่พบ Coil สำหรับ Move"
        )
    )

    # =====================================
    # ORDER+
    # =====================================

    df["Order_Plus"] = np.where(
        df["
