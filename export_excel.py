import io
import pandas as pd


def export_to_excel(df):

    output = io.BytesIO()

    summary = pd.DataFrame({

        "Metric": [
            "Orders",
            "Outstanding",
            "Production Add",
            "NC Coil"
        ],

        "Value": [

            len(df),

            df["Outstanding"].sum()
            if "Outstanding" in df.columns
            else 0,

            df["Production_Add"].sum()
            if "Production_Add" in df.columns
            else 0,

            df["NC"].sum()
            if "NC" in df.columns
            else 0
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
