import streamlit as st
import plotly.express as px


def show_dashboard(df):
    st.subheader("KPI Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Outstanding", f"{df['Outstanding'].sum():,.2f}")
    c2.metric("Coil Inv", f"{df['Coil inv'].sum():,.2f}")
    c3.metric("ผลิตเพิ่ม", f"{df['ผลิตเพิ่ม'].sum():,.2f}")
    c4.metric("Move Coil", f"{df['คอยที่เหลือ พร้อม Move'].sum():,.2f}")

    st.divider()

    st.subheader("Top 10 Outstanding By Buyer")

    buyer_df = (
        df.groupby('Buyer')['Outstanding']
        .sum()
        .reset_index()
        .sort_values('Outstanding', ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        buyer_df,
        x='Buyer',
        y='Outstanding',
        title='Outstanding by Buyer'
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader('Top 10 Outstanding By Customer')

    customer_df = (
        df.groupby('End Cust.')['Outstanding']
        .sum()
        .reset_index()
        .sort_values('Outstanding', ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        customer_df,
        x='End Cust.',
        y='Outstanding',
        title='Outstanding by Customer'
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader('Order Status')

    status_df = (
        df.groupby('Order+')
        .size()
        .reset_index(name='Count')
    )

    fig3 = px.pie(
        status_df,
        names='Order+',
        values='Count',
        title='Order Status'
    )

    st.plotly_chart(fig3, use_container_width=True)
