import streamlit as st


def render_chart(df, chart_config):

    chart_type = chart_config["chart_type"]

    config = chart_config["config"]

    if chart_type == "line":

        st.line_chart(
            df,
            x=config["x"],
            y=config["y"]
        )

    elif chart_type == "bar":

        st.bar_chart(
            df,
            x=config["x"],
            y=config["y"]
        )

    else:

        st.dataframe(df)