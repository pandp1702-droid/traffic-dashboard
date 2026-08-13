import streamlit as st
import plotly.express as px


def show_dashboard(df):

    st.header("Traffic Dashboard")

    # ==========================
    # MAIN KPI
    # ==========================

    c1, c2, c3, c4 = st.columns(4)

    outstanding = (
        df["Outstanding"].sum()
        if "Outstanding" in df.columns
        else 0
    )

    coil_inv = (
        df["Coil_Inv"].sum()
        if "Coil_Inv" in df.columns
        else 0
    )

    production_add = (
        df["Production_Add"].sum()
        if "Production_Add" in df.columns
        else 0
    )

    move_coil = (
        df["Move_Coil"].sum()
        if "Move_Coil" in df.columns
        else 0
    )

    c1.metric(
        "Outstanding",
        f"{outstanding:,.2f}"
    )

    c2.metric(
        "Coil Inventory",
        f"{coil_inv:,.2f}"
    )

    c3.metric(
        "Production Add",
        f"{production_add:,.2f}"
    )

    c4.metric(
        "Move Coil",
        f"{move_coil:,.2f}"
    )

    st.divider()

    # ==========================
    # SUMMARY KPI
    # =================
