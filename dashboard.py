import streamlit as st

def show_dashboard(df):

    st.header("Traffic Dashboard")

    st.metric(
        "Total Orders",
        len(df)
    )

    if "Outstanding" in df.columns:

        st.metric(
            "Outstanding",
            round(
                df["Outstanding"].sum(),
                2
            )
        )

    st.subheader("Data Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )
