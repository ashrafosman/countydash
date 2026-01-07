from typing import Optional

import streamlit as st


def get_access_token() -> Optional[str]:
    try:
        headers = st.context.headers
    except Exception:
        return None

    token = headers.get("X-Forwarded-Access-Token")
    if token:
        return token
    return None
