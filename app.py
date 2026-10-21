import streamlit as st
import pandas as pd

from modules.loader import load_vrm_excel
from modules.plotting import create_plot

st.set_page_config(
    page_title="Victron Analytics",
    layout="wide"
)

st.title("Victron Analytics")

uploaded_file = st.file_uploader(
    "Charger un export VRM Excel",
    type=["xlsx"]
)

if uploaded_file:

    df = load_vrm_excel(uploaded_file)

    st.success(f"{len(df)} lignes chargées")

    columns = [
        col for col in df.columns
        if col != "timestamp"
    ]

    selected_columns = st.multiselect(
        "Mesures à afficher",
        columns
    )

    if selected_columns:

        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Début",
                df["timestamp"].min().date()
            )

        with col2:
            end_date = st.date_input(
                "Fin",
                df["timestamp"].max().date()
            )

        filtered_df = df[
            (df["timestamp"].dt.date >= start_date)
            &
            (df["timestamp"].dt.date <= end_date)
        ]

        fig = create_plot(
            filtered_df,
            selected_columns
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(filtered_df)