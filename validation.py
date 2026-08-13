import pandas as pd


def validate_data(df):

    issues = []

    if "Outstanding" in df.columns:

        neg = df[df["Outstanding"] < 0]

        if len(neg) > 0:
            issues.append(
                f"Negative Outstanding found: {len(neg)} rows"
            )

    if "OrderNo" in df.columns:

        dup = df[df["OrderNo"].duplicated()]

        if len(dup) > 0:
            issues.append(
                f"Duplicate OrderNo found: {len(dup)} rows"
            )

    if "Buyer" in df.columns:

        blank = df["Buyer"].isna().sum()

        if blank > 0:
            issues.append(
                f"Blank Buyer found: {blank} rows"
            )

    if "End Cust." in df.columns:

        blank = df["End Cust."].isna().sum()

        if blank > 0:
            issues.append(
                f"Blank Customer found: {blank} rows"
            )

    status = "PASS" if len(issues) == 0 else "FAIL"

    return {
        "status": status,
        "issues": issues,
        "issue_count": len(issues)
    }
