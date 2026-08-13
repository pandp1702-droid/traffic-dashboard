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

                df["Move_Coil"].sum()
                if "Move_Coil" in df.columns
                else 0,

                len(df),

                df["Buyer"].nunique()
                if "Buyer" in df.columns
                else 0,

                df["End Cust."].nunique()
                if "End Cust." in df.columns
                else 0,

                (
                    df["Order_Status"] == "OPEN"
                ).sum()
                if "Order_Status" in df.columns
                else 0,

                (
                    df["Order_Status"] == "CLOSED"
                ).sum()
                if "Order_Status" in df.columns
                else 0,
            ]
        }
    )

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # Summary Sheet
        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        # Data Sheet
        df.to_excel(
            writer,
            sheet_name="Data",
            index=False
        )

        # Top Buyer Sheet
        if (
            "Buyer" in df.columns
            and "Outstanding" in df.columns
        ):

            buyer_summary = (
                df.groupby("Buyer")["Outstanding"]
                .sum()
                .reset_index()
                .sort_values(
                    "Outstanding",
                    ascending=False
                )
            )

            buyer_summary.to_excel(
                writer,
                sheet_name="Buyer Summary",
                index=False
            )

        # Customer Sheet
        if (
            "End Cust." in df.columns
            and "Outstanding" in df.columns
        ):

            customer_summary = (
                df.groupby("End Cust.")["Outstanding"]
                .sum()
                .reset_index()
                .sort_values(
                    "Outstanding",
                    ascending=False
                )
            )

            customer_summary.to_excel(
                writer,
                sheet_name="Customer Summary",
                index=False
            )

    output.seek(0)

    return output
