import streamlit as st

from auth import get_access_token
from data_access import get_data_source_status


@st.cache_data(ttl=60)
def _cached_status(access_token: str | None):
    return get_data_source_status(access_token=access_token)


def render_data_source_status() -> None:
    access_token = get_access_token()
    status = _cached_status(access_token)
    mode = status.get("mode")
    if mode == "spark":
        st.sidebar.success(f"Data source: Spark ({status.get('details')})")
        return
    if mode == "sql":
        message = f"Data source: Delta via SQL ({status.get('details')})"
        row_count = status.get("row_count")
        if isinstance(row_count, int):
            message = f"{message} - {row_count:,} rows"
        st.sidebar.success(message)
        return

    st.sidebar.warning("Data source: Sample data")
    error = status.get("error")
    if error:
        st.sidebar.caption(error)
