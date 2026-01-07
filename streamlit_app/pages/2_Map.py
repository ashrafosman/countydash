import streamlit as st

from data_access import load_counties
from ui_helpers import render_data_source_status

st.set_page_config(page_title="County Map", layout="wide")

render_data_source_status()

st.title("California County Map")
st.caption("Click a county in the main dashboard to view details.")

counties = load_counties()
map_data = counties[["name", "latitude", "longitude"]].dropna()

if map_data.empty:
    st.info("No geocoded county data available.")
else:
    st.map(map_data.rename(columns={"latitude": "lat", "longitude": "lon"}))
