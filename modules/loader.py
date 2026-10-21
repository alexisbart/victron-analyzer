import pandas as pd


def load_vrm_excel(file):

    raw = pd.read_excel(
        file,
        sheet_name=0,
        header=None,
        engine="openpyxl"
    )

    device_row = raw.iloc[1]
    metric_row = raw.iloc[2]

    column_names = []

    for device, metric in zip(device_row, metric_row):

        if pd.isna(metric):
            column_names.append("Unknown")
            continue

        if pd.isna(device):
            column_names.append(str(metric))
        else:
            column_names.append(
                f"{device} | {metric}"
            )

    data = raw.iloc[4:].copy()

    data.columns = column_names

    timestamp_column = data.columns[0]

    data.rename(
        columns={
            timestamp_column: "timestamp"
        },
        inplace=True
    )

    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["timestamp"]
    )

    return data