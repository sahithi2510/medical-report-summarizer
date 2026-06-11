import streamlit as st
import plotly.express as px


def display_charts(results_df):

    if results_df.empty:
        return

    st.subheader("📊 Medical Analysis Dashboard")

    fig = px.bar(
        results_df,
        x="Test",
        y="Value",
        color="Status",
        text="Value",
        title="Detected Medical Parameters"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=550,
        xaxis_title="Medical Test",
        yaxis_title="Measured Value"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    status_counts = (
        results_df["Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    pie_fig = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Result Distribution"
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )