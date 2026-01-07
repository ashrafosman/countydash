import pandas as pd
import streamlit as st

from data.product_backlog import PRODUCT_BACKLOG

st.set_page_config(page_title="Product Backlog", layout="wide")

st.title("Product Backlog")
st.caption("Engineering backlog for the county dashboard program.")

df = pd.DataFrame(PRODUCT_BACKLOG)
df["completion_pct"] = (df["completed"] / df["stories"] * 100).round(0)

st.dataframe(df, hide_index=True, use_container_width=True)

for _, row in df.iterrows():
    st.markdown(f"**{row['epic']}**")
    st.progress(min(int(row["completion_pct"]), 100))
