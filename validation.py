import pandas as pd

def validate_data(df):
    issues = []

    # Outstanding ติดลบ
    if 'Outstanding' in df.columns:
        neg = df[df['Outstanding'] < 0]
        if len(neg) > 0:
            issues.append(f'พบ Outstanding ติดลบ {len(neg)} รายการ')

    # Order ซ้ำ
    if 'OrderNo' in df.columns:
        dup = df[df['OrderNo'].duplicated()]
        if len(dup) > 0:
            issues.append(f'พบ OrderNo ซ้ำ {len(dup)} รายการ')

    # Buyer ว่าง
    if 'Buyer' in df.columns:
        blank = df['Buyer'].isna().sum()
        if blank > 0:
            issues.append(f'พบ Buyer ว่าง {blank} รายการ')

    # End Customer ว่าง
    if 'End Cust.' in df.columns:
        blank = df['End Cust.'].isna().sum()
        if blank > 0:
            issues.append(f'พบ End Customer ว่าง {blank} รายการ')

    # Order ปิดแต่ยังมี Coil
    if 'ปิดOrder' in df.columns and 'Coil inv' in df.columns:
        invalid = df[(df['ปิดOrder'] == 'ปิด') & (df['Coil inv'] > 0)]
        if len(invalid) > 0:
            issues.append(f'พบ Order ปิดแต่ยังมี Coil {len(invalid)} รายการ')

    status = 'PASS' if len(issues) == 0 else 'FAIL'

    return {
        'status': status,
        'issues': issues,
        'issue_count': len(issues)
    }
