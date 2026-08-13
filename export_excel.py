import io
import pandas as pd


def export_to_excel(df):

    output = io.BytesIO()

    summary = pd.DataFrame({
        "Metric": [
            "Outstanding",
            "Coil Inventory",
            "Production Add",
            "Move Coil"
        ],
        "Value": [
            df["Outstanding"].sum(),
            df["Coil_Inv"].sum(),
            df["Production_Add"].sum(),
            df["Move_Coil"].sum()
        ]
    })

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        df.to_excel(
            writer,
            sheet_name="Data",
            index=False
        )

    output.seek(0)

    return output
