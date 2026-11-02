import pandas as pd
import plotly.graph_objects as go


RULE_MAP = {
    "5 min": "5min",
    "15 min": "15min",
    "30 min": "30min",
    "1 h": "1h",
    "2 h": "2h",
    "4 h": "4h",
    "1 jour": "1D"
}


def normalize(series):

    series = pd.to_numeric(
        series,
        errors="coerce"
    )

    min_value = series.min()
    max_value = series.max()

    if pd.isna(min_value):
        return series

    if min_value == max_value:
        return series * 0

    return (
        series - min_value
    ) / (
        max_value - min_value
    )


def is_power_column(column):

    return (
        "(W)" in column
        or "(kW)" in column
    )


def resample_column(
    df,
    column,
    delta_t
):

    temp = df.copy()

    temp[column] = pd.to_numeric(
        temp[column],
        errors="coerce"
    )

    resampled = (
        temp
        .set_index("timestamp")[[column]]
        .resample(
            RULE_MAP[delta_t]
        )
        .mean()
        .reset_index()
    )

    return resampled


def create_normalized_plot(
    df,
    columns,
    delta_t
):

    fig = go.Figure()

    for column in columns:

        try:

            temp = resample_column(
                df,
                column,
                delta_t
            )

            y = normalize(
                temp[column]
            )

            if is_power_column(column):

                fig.add_trace(
                    go.Bar(
                        x=temp["timestamp"],
                        y=y,
                        name=column,
                        opacity=0.6,
                        hovertemplate=
                        "%{y:.3f}<br>"
                        + column +
                        "<extra></extra>"
                    )
                )

            else:

                fig.add_trace(
                    go.Scatter(
                        x=temp["timestamp"],
                        y=y,
                        mode="lines",
                        name=column,
                        hovertemplate=
                        "%{y:.3f}<br>"
                        + column +
                        "<extra></extra>"
                    )
                )

        except Exception:
            continue

    fig.update_layout(
        title="Comparaison des tendances",
        xaxis_title="Temps",
        yaxis_title="Normalisé (0 → 1)",
        hovermode="x unified",
        height=700
    )

    return fig


def create_real_plot(
    df,
    columns,
    delta_t
):

    fig = go.Figure()

    for column in columns:

        try:

            temp = resample_column(
                df,
                column,
                delta_t
            )

            if is_power_column(column):

                fig.add_trace(
                    go.Bar(
                        x=temp["timestamp"],
                        y=temp[column],
                        name=column,
                        opacity=0.6,
                        hovertemplate=
                        "%{y}<br>"
                        + column +
                        "<extra></extra>"
                    )
                )

            else:

                fig.add_trace(
                    go.Scatter(
                        x=temp["timestamp"],
                        y=temp[column],
                        mode="lines",
                        name=column,
                        hovertemplate=
                        "%{y}<br>"
                        + column +
                        "<extra></extra>"
                    )
                )

        except Exception:
            continue

    fig.update_layout(
        title="Valeurs réelles",
        xaxis_title="Temps",
        yaxis_title="Valeur",
        hovermode="x unified",
        height=700
    )

    return fig