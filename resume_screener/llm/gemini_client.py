"""
Gemini client setup.

API key resolution order (first one found wins):
1. st.secrets["GEMINI_API_KEY"]   (Streamlit Cloud / .streamlit/secrets.toml)
2. os.environ["GEMINI_API_KEY"]   (.env / shell env var)
3. Manually typed into the sidebar for that session only (never persisted)

Uses the `google-genai` SDK (the current unified Google GenAI SDK). If you're
setting this up fresh, run: pip install google-genai
"""

import os
import streamlit as st


def get_api_key() -> str | None:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass  # no secrets.toml present locally — that's fine, fall through

    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    return st.session_state.get("gemini_api_key_manual")


def has_api_key() -> bool:
    return bool(get_api_key())


def get_client():
    """Returns a configured genai.Client, or None if no API key is available."""
    api_key = get_api_key()
    if not api_key:
        return None

    from google import genai
    return genai.Client(api_key=api_key)
