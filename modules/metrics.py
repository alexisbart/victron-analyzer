import pandas as pd


def summarize_series(df, column):

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    return {
        "min": series.min(),
        "max": series.max(),
        "avg": series.mean()
    }


def get_min(df, column):

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).min()


def get_max(df, column):

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).max()


def get_average(df, column):

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).mean()