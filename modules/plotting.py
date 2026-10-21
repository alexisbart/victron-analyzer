import plotly.graph_objects as go


def create_plot(df, columns):

    fig = go.Figure()

    for column in columns:

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df[column],
                mode="lines",
                name=column
            )
        )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Temps",
        yaxis_title="Valeur"
    )

    return fig