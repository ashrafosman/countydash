import streamlit as st

st.set_page_config(page_title="Help", layout="wide")

st.title("Help & Support")

faqs = [
    (
        "How do I interpret the penetration rate data?",
        "Penetration rate represents the share of Medi-Cal enrollees receiving services.",
    ),
    (
        "What is the difference between MH and SUD services?",
        "MH covers mental health care; SUD covers substance use treatment.",
    ),
    (
        "How often is the data updated?",
        "Quarterly refreshes with annual validation cycles.",
    ),
]

for question, answer in faqs:
    with st.expander(question):
        st.write(answer)

st.markdown("### Contact Support")
with st.form("support"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Support ticket submitted (placeholder).")
