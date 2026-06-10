import streamlit as st


def render_report(result):

    analytics = result.get("analytics", {})

    st.write("### Analytics")

    if analytics:
        st.write(analytics)
    else:
        st.write("No analytics available")