import io
import pandas as pd


def export_to_excel(df):

    output = io.BytesIO()

    summary = pd.DataFrame(
        {
            "Metric": [
                "Outstanding",
                "Coil Inventory",
                "Production Add",
                "Move Coil",
                "Total Orders",
                "Total Buyers",
                "Total Customers",
                "Open Orders",
                "Closed Orders"
            ],
            "Value": [

                df["Outstanding"].sum()
                if "Outstanding" in df.columns
                else 0,

                df["Coil_Inv"].sum()
                if "Coil_Inv" in df.columns
                else 0,

                df["Production_Add"].sum()
                if "Production_Add" in df.columns
                else 0,

                df["Move_Coil"].sum
