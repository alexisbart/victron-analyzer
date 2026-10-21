def filter_dates(df, start, end):

    return df[
        (df["timestamp"] >= start)
        &
        (df["timestamp"] <= end)
    ]