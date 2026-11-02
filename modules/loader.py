import pandas as pd


def load_vrm_excel(file):
    """
    Charge un export Victron VRM.

    Structure attendue :

    Ligne 0 : vide
    Ligne 1 : Device
    Ligne 2 : Metric
    Ligne 3 : Unit
    Ligne 4+ : Data
    """

    raw = pd.read_excel(
        file,
        sheet_name=0,
        header=None,
        engine="openpyxl"
    )

    device_row = raw.iloc[1]
    metric_row = raw.iloc[2]
    unit_row = raw.iloc[3]

    column_names = []

    for device, metric, unit in zip(
        device_row,
        metric_row,
        unit_row
    ):

        if pd.isna(metric):
            column_names.append("Unknown")
            continue

        device = "" if pd.isna(device) else str(device)
        metric = str(metric)

        if pd.isna(unit):
            unit = ""
        else:
            unit = str(unit).strip()

        if device:

            if unit:
                column_name = (
                    f"{device} | {metric} ({unit})"
                )
            else:
                column_name = (
                    f"{device} | {metric}"
                )

        else:

            if unit:
                column_name = (
                    f"{metric} ({unit})"
                )
            else:
                column_name = metric

        column_names.append(column_name)

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

    data.reset_index(
        drop=True,
        inplace=True
    )

    return data