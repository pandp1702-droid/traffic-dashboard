import streamlit as st

def show_dashboard(df):

    st.header("Traffic Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Outstanding",
        round(df["Outstanding"].sum(), 2)
        if "Outstanding" in df.columns
        else 0
    )

    col2.metric(
        "Coil Inventory",
        round(df["Coil_Inv"].sum(), 2)
        if "Coil_Inv" in df.columns
        else 0
    )

    col3.metric(
        "Production Add",
        round(df["Production_Add"].sum(), 2)
        if "Production_Add" in df.columns
        else 0
    )

    col4.metric(
        "Move Coil",
        round(df["Move_Coil"].sum(), 2)
        if "Move_Coil" in df.columns
        else 0
    )

    st.divider()

    st.dataframe(
        df.head(100),
        use_container_width=True
    )
