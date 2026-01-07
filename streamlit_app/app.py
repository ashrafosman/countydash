import json

import pandas as pd
import streamlit as st

from auth import get_access_token
from data_access import add_review_comment, load_counties, load_review_comments
from ui_helpers import render_data_source_status
from utils import format_number

st.set_page_config(page_title="DHCS County Dashboard", layout="wide")

render_data_source_status()

st.title("Behavioral Health Transformation County Dashboard")

access_token = get_access_token()
counties = load_counties(access_token=access_token)
county_lookup = counties.set_index("county_id")

st.sidebar.header("Filters")
comparison_mode = st.sidebar.checkbox("Comparison mode")

default_county = "los-angeles" if "los-angeles" in counties["county_id"].values else counties["county_id"].iloc[0]

if comparison_mode:
    selected_ids = st.sidebar.multiselect(
        "Select counties",
        options=counties["county_id"].tolist(),
        default=[default_county],
        format_func=lambda cid: county_lookup.loc[cid, "name"],
    )
else:
    selected_ids = [
        st.sidebar.selectbox(
            "Select county",
            options=counties["county_id"].tolist(),
            index=counties["county_id"].tolist().index(default_county),
            format_func=lambda cid: county_lookup.loc[cid, "name"],
        )
    ]

if not selected_ids:
    st.warning("Select at least one county to view data.")
    st.stop()

current = county_lookup.loc[selected_ids[0]].to_dict()

st.subheader(current["name"])
st.caption("Comprehensive behavioral health profile and analytics dashboard")

metric_cols = st.columns(4)
metric_cols[0].metric("Total Population", format_number(current.get("population")))
metric_cols[1].metric("Medi-Cal Enrolled", format_number(current.get("medi_cal_enrolled")))
metric_cols[2].metric("BH Clients (Annual)", format_number(current.get("bh_services_annual")))
metric_cols[3].metric("Annual Expenditures", f"${format_number(current.get('annual_expenditures'))}")

if comparison_mode and len(selected_ids) > 1:
    comparison = counties[counties["county_id"].isin(selected_ids)][
        ["name", "population", "medi_cal_enrolled", "bh_services_annual", "annual_expenditures"]
    ].copy()
    comparison = comparison.rename(
        columns={
            "medi_cal_enrolled": "Medi-Cal Enrolled",
            "bh_services_annual": "BH Clients (Annual)",
            "annual_expenditures": "Annual Expenditures",
        }
    )
    st.markdown("### Comparison")
    st.dataframe(comparison, use_container_width=True, hide_index=True)

tabs = st.tabs(
    [
        "Overview",
        "Demographics",
        "Behavioral Health",
        "Integrated Plan",
        "Expenditures",
        "Homelessness",
        "Performance",
    ]
)

demographics = current.get("demographics_json") or {}
behavioral = current.get("behavioral_health_json") or {}
expenditures = current.get("expenditures_json") or {}
homelessness = current.get("homelessness_json") or {}
integrated = current.get("integrated_plan_json") or {}
performance = current.get("performance_json") or {}

with tabs[0]:
    st.markdown("### Contact Information")
    contact_cols = st.columns(2)
    contact_cols[0].write(current.get("contact_department", ""))
    contact_cols[0].write(current.get("contact_address", ""))
    contact_cols[0].write(current.get("contact_city", ""))
    contact_cols[1].write(current.get("contact_phone", ""))
    contact_cols[1].write(current.get("contact_email", ""))

with tabs[1]:
    st.markdown("### Population by Age")
    age_data = pd.DataFrame(demographics.get("population_by_age", []))
    if not age_data.empty:
        st.bar_chart(age_data.set_index("age")["population"])
    st.markdown("### Population by Race/Ethnicity")
    ethnicity_data = pd.DataFrame(demographics.get("population_by_ethnicity", []))
    if not ethnicity_data.empty:
        st.bar_chart(ethnicity_data.set_index("ethnicity")["value"])

with tabs[2]:
    st.markdown("### Penetration Rates")
    penetration = pd.DataFrame(behavioral.get("penetration_rates", []))
    if not penetration.empty:
        st.dataframe(penetration, hide_index=True, use_container_width=True)
    st.markdown("### Access Metrics")
    access_metrics = pd.DataFrame(behavioral.get("access_metrics", []))
    if not access_metrics.empty:
        st.line_chart(access_metrics.set_index("quarter"))

with tabs[3]:
    st.markdown("### Integrated Plan Status")
    st.write(f"Status: {integrated.get('status', 'N/A')}")
    st.write(f"Phase: {integrated.get('phase', 'N/A')}")
    if integrated.get("completion_date"):
        st.write(f"Completion Date: {integrated.get('completion_date')}")
    allocations = pd.DataFrame(integrated.get("budget_allocations", []))
    if not allocations.empty:
        st.markdown("### Budget Allocations")
        st.dataframe(allocations, hide_index=True, use_container_width=True)

with tabs[4]:
    st.markdown("### Expenditures by Category")
    by_category = pd.DataFrame(expenditures.get("by_category", []))
    if not by_category.empty:
        st.dataframe(by_category, hide_index=True, use_container_width=True)
    trend = pd.DataFrame(expenditures.get("trend_data", []))
    if not trend.empty:
        st.markdown("### Expenditure Trend")
        st.line_chart(trend.set_index("year"))

with tabs[5]:
    st.markdown("### Homelessness Metrics")
    st.metric("HDIS Enrolled", format_number(homelessness.get("hdis_enrolled")))
    housing = pd.DataFrame(homelessness.get("housing_interventions", []))
    if not housing.empty:
        st.dataframe(housing, hide_index=True, use_container_width=True)

with tabs[6]:
    st.markdown("### Performance Metrics")
    phase2 = pd.DataFrame(performance.get("phase2_measures", []))
    if not phase2.empty:
        st.dataframe(phase2, hide_index=True, use_container_width=True)
    perf_cols = st.columns(2)
    perf_cols[0].metric("Compliance Rate", f"{performance.get('compliance_rate', 0)}%")
    perf_cols[1].metric("Monitoring Reports", performance.get("monitoring_reports", 0))

st.markdown("---")
st.markdown("### Review Comments")
comments = load_review_comments(page_url="county-profile", access_token=access_token)
if comments.empty:
    st.info("No review comments yet.")
else:
    st.dataframe(
        comments[["element_name", "comment_text", "author", "created_at"]],
        hide_index=True,
        use_container_width=True,
    )

with st.expander("Add a review comment"):
    with st.form("add-comment"):
        element_name = st.text_input("Element")
        author = st.text_input("Author")
        comment_text = st.text_area("Comment")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not element_name or not author or not comment_text:
                st.warning("Element, author, and comment are required.")
            else:
                saved = add_review_comment(
                    element_name=element_name,
                    page_url="county-profile",
                    comment_text=comment_text,
                    author=author,
                    access_token=access_token,
                )
                if saved:
                    st.success("Comment saved to Delta table.")
                else:
                    st.info("Unable to save comment. Check Delta table connectivity.")
