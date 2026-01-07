import pandas as pd
import streamlit as st

st.set_page_config(page_title="Users", layout="wide")

st.title("User Management")

users = pd.DataFrame(
    [
        {
            "name": "Abhay Shekatkar",
            "email": "abhay.shekatkar@dhcs.ca.gov",
            "role": "admin",
            "county": "Los Angeles",
            "status": "active",
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@dhcs.ca.gov",
            "role": "analyst",
            "county": "Los Angeles",
            "status": "active",
        },
        {
            "name": "Michael Chen",
            "email": "michael.chen@dhcs.ca.gov",
            "role": "analyst",
            "county": "San Francisco",
            "status": "active",
        },
    ]
)

st.dataframe(users, hide_index=True, use_container_width=True)

with st.expander("Add user"):
    with st.form("add-user"):
        name = st.text_input("Full name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["admin", "analyst", "viewer"])
        county = st.text_input("County")
        submitted = st.form_submit_button("Add")
        if submitted:
            st.info("User creation is a placeholder in Streamlit.")
