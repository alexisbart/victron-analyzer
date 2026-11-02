import datetime

import pandas as pd
import streamlit as st

from modules.loader import load_vrm_excel
from modules.plotting import (
    create_normalized_plot,
    create_real_plot
)

st.set_page_config(
    page_title="Victron Analytics",
    layout="wide"
)

st.title("Victron Analytics")

uploaded_file = st.file_uploader(
    "Charger un export VRM",
    type=["xlsx"]
)

if uploaded_file:

    df = load_vrm_excel(uploaded_file)

    st.success(
        f"{len(df):,} lignes chargées"
    )

    columns = [
        col
        for col in df.columns
        if col != "timestamp"
    ]

    st.sidebar.header("Filtres")

    start_date = st.sidebar.date_input(
        "Date début",
        value=df["timestamp"].min().date()
    )

    start_time = st.sidebar.time_input(
        "Heure début",
        value=df["timestamp"].min().time()
    )

    end_date = st.sidebar.date_input(
        "Date fin",
        value=df["timestamp"].max().date()
    )

    end_time = st.sidebar.time_input(
        "Heure fin",
        value=df["timestamp"].max().time()
    )

    start_datetime = datetime.datetime.combine(
        start_date,
        start_time
    )

    end_datetime = datetime.datetime.combine(
        end_date,
        end_time
    )

    delta_t = st.sidebar.selectbox(
        "Delta t",
        [
            "5 min",
            "15 min",
            "30 min",
            "1 h",
            "2 h",
            "4 h",
            "1 jour"
        ]
    )

    selected_columns = st.sidebar.multiselect(
        "Mesures à afficher",
        columns
    )

    filtered_df = df[
        (df["timestamp"] >= pd.Timestamp(start_datetime))
        &
        (df["timestamp"] <= pd.Timestamp(end_datetime))
    ].copy()

    st.info(
        f"{len(filtered_df):,} points affichés"
    )

    if selected_columns:

        st.subheader(
            "Comparaison des tendances (normalisé)"
        )

        fig_norm = create_normalized_plot(
            filtered_df,
            selected_columns,
            delta_t
        )

        st.plotly_chart(
            fig_norm,
            use_container_width=True
        )

        st.subheader(
            "Valeurs réelles"
        )

        fig_real = create_real_plot(
            filtered_df,
            selected_columns,
            delta_t
        )

        st.plotly_chart(
            fig_real,
            use_container_width=True
        )

    else:

        st.warning(
            "Sélectionnez au moins une mesure."
        )

    with st.expander(
        "Aperçu des données"
    ):

        st.dataframe(
            filtered_df.head(100)
        )