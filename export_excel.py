import io
import pandas as pd


def export_to_excel(df):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # Summary
        summary = pd.DataFrame({
            "Metric": [
                "Orders",
                "Outstanding"
            ],
            "Value": [
                len(df),
                df["Outstanding"].sum()
                if "Outstanding" in df.columns
                else 0
            ]
        })

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        # Data
        df.to_excel(
            writer,
            sheet_name="Data",
            index=False
        )

    output.seek(0)

    return output.getvalue()
