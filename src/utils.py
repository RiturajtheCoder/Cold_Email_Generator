from __future__ import annotations

import html
from typing import Any

import streamlit as st


def init_session_state() -> None:
    defaults = {
        "candidate": {},
        "target": {"tone": "Professional", "length": "Medium"},
        "generated_email": "",
        "subject_lines": [],
        "analysis": {},
        "generated_data": {},
        "generation_history": [],
        "shareable_link": "",
        "force_mode": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def parse_multiline_items(text: str) -> list[str]:
    if not text:
        return []
    return [line.strip() for line in text.replace(",", "\n").splitlines() if line.strip()]


def as_clean_list(text: str) -> list[str]:
    return parse_multiline_items(text)


def copy_button_html(text: str) -> str:
    safe = html.escape(text)
    return f"""
    <button class="copy-btn" onclick="navigator.clipboard.writeText(`{safe}`)">
        Copy Email
    </button>
    """


def format_word_count(count: Any) -> str:
    try:
        return f"{int(count)} words"
    except Exception:
        return "0 words"


def safe_truncate(text: str, max_len: int = 42) -> str:
    if not text:
        return "Not set"
    return text if len(text) <= max_len else text[: max_len - 1] + "…"
