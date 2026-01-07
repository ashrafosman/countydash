import json

import streamlit as st

from auth import get_access_token
from data_access import load_counties
from ui_helpers import render_data_source_status

st.set_page_config(page_title="Export", layout="wide")

render_data_source_status()

st.title("Export County Report")
st.caption("Generate a lightweight export for the selected county.")

counties = load_counties(access_token=get_access_token())
county_lookup = counties.set_index("county_id")

selected_id = st.selectbox(
    "Select county",
    options=counties["county_id"].tolist(),
    format_func=lambda cid: county_lookup.loc[cid, "name"],
)

sections = st.multiselect(
    "Sections to include",
    [
        "overview",
        "demographics",
        "behavioral_health",
        "integrated_plan",
        "expenditures",
        "homelessness",
        "performance",
    ],
    default=["overview", "demographics", "behavioral_health"],
)

export_format = st.selectbox("Format", ["JSON", "CSV"])

if st.button("Generate Export"):
    county = county_lookup.loc[selected_id].to_dict()
    payload = {"county_id": selected_id, "name": county.get("name")}
    for section in sections:
        key = f"{section}_json"
        payload[section] = county.get(key) or {}

    if export_format == "JSON":
        st.download_button(
            "Download JSON",
            data=json.dumps(payload, indent=2, default=str),
            file_name=f"{selected_id}-report.json",
        )
    else:
        st.download_button(
            "Download CSV",
            data=counties[counties["county_id"] == selected_id].to_csv(index=False),
            file_name=f"{selected_id}-report.csv",
        )
