import io
import pandas as pd


def export_to_excel(df):
    """Export DataFrame to Excel in memory"""

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            sheet_name="Data",
            index=False
        )

    output.seek(0)
    return output
