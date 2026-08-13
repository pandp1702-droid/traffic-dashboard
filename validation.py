import pandas as pd


def validate_data(df):

    issues = []

    # Negative Outstanding
    if "Outstanding" in df.columns:

        negative_rows = df[
            df["Outstanding"] < 0
        ]

        if len(negative_rows) > 0:

            issues.append(
                f"Negative Outstanding found: {len(negative_rows)} rows"
            )

    # Duplicate Order + Item
    if (
        "OrderNo" in df.columns
        and "Item" in df.columns
    ):

        order_item_key = (
            df["OrderNo"].astype(str)
            + "_"
            + df["Item"].astype(str)
        )

        duplicate_rows = df[
            order_item_key.duplicated()
        ]

        if len(duplicate_rows) > 0:

            issues.append(
                f"Duplicate Order+Item found: {len(duplicate_rows)} rows"
            )

    # Blank Buyer
    if "Buyer" in df.columns:

        blank_buyer = (
            df["Buyer"]
            .isna()
            .sum()
        )

        if blank_buyer > 0:

            issues.append(
                f"Blank Buyer found: {blank_buyer} rows"
            )

    # Blank Customer
    if "End Cust." in df.columns:

        blank_customer = (
            df["End Cust."]
            .isna()
            .sum()
        )

        if blank_customer > 0:

            issues.append(
                f"Blank Customer found: {blank_customer} rows"
            )

    # Missing Order Number
    if "OrderNo" in df.columns:

        blank_order = (
            df["OrderNo"]
            .isna()
            .sum()
        )

        if blank_order > 0:

            issues.append(
                f"Blank OrderNo found: {blank_order} rows"
            )

    # Missing Product Code
    if "Prod Cd" in df.columns:

        blank_product = (
            df["Prod Cd"]
            .isna()
            .sum()
        )

        if blank_product > 0:

            issues.append(
                f"Blank Product Code found: {blank_product} rows"
            )

    # Closed order with inventory
    if (
        "Order_Status" in df.columns
        and "Coil_Inv" in df.columns
    ):

        invalid_rows = df[
            (df["Order_Status"] == "CLOSED")
            &
            (df["Coil_Inv"] > 0)
        ]

        if len(invalid_rows) > 0:

            issues.append(
                f"Closed Order With Inventory: {len(invalid_rows)} rows"
            )

    status = "PASS"

    if len(issues) > 0:
        status = "FAIL"

    return {
        "status": status,
        "issue_count": len(issues),
        "issues": issues
    }
