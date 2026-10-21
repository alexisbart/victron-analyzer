import pandas as pd


def summarize_series(df, column):

    return {
        "min": df[column].min(),
        "max": df[column].max(),
        "avg": df[column].mean(),
    }