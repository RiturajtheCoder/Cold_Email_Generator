import os

import streamlit as st

try:
    import google.genai as genai
except Exception:  # pragma: no cover - handled gracefully at runtime
    genai = None


def is_api_key_configured() -> bool:
    return bool(get_api_key())


def get_api_key() -> str:
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


def get_client():
    if genai is None:
        raise ImportError(
            "The Gemini SDK is not installed correctly. Run `pip install -r requirements.txt`."
        )
    api_key = get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to .env or Streamlit secrets.")
    return genai.Client(api_key=api_key)


def get_api_status() -> str:
    if not get_api_key():
        return "Missing GEMINI_API_KEY"
    return "Ready"
