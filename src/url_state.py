from urllib.parse import urlencode

import streamlit as st


def apply_query_params(session_state) -> None:
    qp = st.query_params
    target = session_state.target
    if qp.get("company"):
        target["company"] = qp.get("company", "")
    if qp.get("role"):
        target["role"] = qp.get("role", "")
    if qp.get("tone"):
        target["tone"] = qp.get("tone", "Professional")
    if qp.get("length"):
        target["length"] = qp.get("length", "Medium")


def build_shareable_query_params(session_state) -> str:
    params = {
        "company": session_state.target.get("company", ""),
        "role": session_state.target.get("role", ""),
        "tone": session_state.target.get("tone", ""),
        "length": session_state.target.get("length", ""),
    }
    clean = {k: v for k, v in params.items() if v}
    st.query_params.clear()
    st.query_params.update(clean)
    return f"?{urlencode(clean)}" if clean else "?"
