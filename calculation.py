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
    # MOVE STATUS
    # =====================================

    df["Move_Status"] = ""

    move_out_mask = (
        df["Move_Available"] > 0
    )

    df.loc[
        move_out_mask,
        "Move_Status"
    ] = "Move Out"

    move_in_mask = (
        df["Outstanding"] > 0
    )

    df.loc[
        move_in_mask,
        "Move_Status"
    ] = np.where(
        df.loc[
            move_in_mask,
            "Move_Available"
        ] > 0,
        "Move In",
        "ผลิตเพิ่ม"
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
        "สามารถ Move Coil ได้",
        np.where(
            df["Move_Coil_Result"] == "Move Coil + ผลิตเพิ่ม",
            "Move Coil ได้บางส่วน ต้องผลิตเพิ่ม",
            "ไม่พบ Coil สำหรับ Move ต้องผลิตเพิ่ม"
        )
    )

    # =====================================
    # ORDER+
    # =====================================

    df["Order_Plus"] = np.where(
        df["Production_Add"] > 3.999,
        "YES",
        "NO"
    )

    # =====================================
    # CLOSE ORDER
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
    # AGING
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

        df["Old_Order"] 
