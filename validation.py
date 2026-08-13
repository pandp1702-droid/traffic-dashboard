import pandas as pd


def validate_data(df):

    issues = []

    # Check negative outstanding
    if "Outstanding" in df.columns:

        negative_rows = df[df["Outstanding"] < 0]

        if len(negative_rows) > 0:
            issues.append(
                f"Negative Outstanding found: {len(negative_rows)} rows"
            )

    # Check duplicate order number
    if "OrderNo + Item" in df.columns:

        duplicate_rows = df[df["OrderNo"].duplicated()]

        if len(duplicate_rows) > 0:
            issues.append(
                f"Duplicate OrderNo found: {len(duplicate_rows)} rows"
            )

    # Check blank buyer
    if "Buyer" in df.columns:

        blank_buyer = df["Buyer"].isna().sum()

        if blank_buyer > 0:
            issues.append(
                f"Blank Buyer found: {blank_buyer} rows"
            )

    # Check blank customer
    if "End Cust." in df.columns:

        blank_customer = df["End Cust."].isna().sum()

        if blank_customer > 0:
            issues.append(
                f"Blank Customer found: {blank_customer} rows"
            )

    # Check closed order with inventory
    if (
        "Close_Order" in df.columns
        and "Coil_Inv" in df.columns
    ):

        invalid_rows = df[
            (df["Close_Order"] == "CLOSED")
            & (df["Coil_Inv"] > 0)
        ]

        if len(invalid_rows) > 0:
            issues.append(
                f"Closed order with inventory found: {len(invalid_rows)} rows"
            )

    status = "PASS"

    if len(issues) > 0:
        status = "FAIL"

    return {
        "status": status,
        "issue_count": len(issues),
        "issues": issues
    }
