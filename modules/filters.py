def filter_dates(
    df,
    start_datetime,
    end_datetime
):

    return df[
        (df["timestamp"] >= start_datetime)
        &
        (df["timestamp"] <= end_datetime)
    ]