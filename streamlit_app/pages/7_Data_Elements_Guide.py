import streamlit as st

from ui_helpers import render_data_source_status

st.set_page_config(page_title="Data Elements Guide", layout="wide")

render_data_source_status()

st.title("Data Elements Guide")

elements = [
    {
        "section": "Overview",
        "name": "Total Population",
        "description": "Total county population based on census estimates.",
        "source": "U.S. Census Bureau",
    },
    {
        "section": "Overview",
        "name": "Medi-Cal Enrollment",
        "description": "Number of Medi-Cal enrollees in the county.",
        "source": "DHCS Administrative Data",
    },
    {
        "section": "Demographics",
        "name": "Population by Age",
        "description": "Population distribution across age bands.",
        "source": "California Dept. of Finance",
    },
    {
        "section": "Behavioral Health",
        "name": "Penetration Rate",
        "description": "Percent of Medi-Cal enrollees receiving services.",
        "source": "Claims and encounter data",
    },
]

query = st.text_input("Search data elements")

for element in elements:
    if query and query.lower() not in element["name"].lower():
        continue
    with st.expander(f"{element['section']} · {element['name']}"):
        st.write(element["description"])
        st.caption(f"Source: {element['source']}")
