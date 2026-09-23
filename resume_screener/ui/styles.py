import streamlit as st
from ui.theme import inject_theme


def render_header():
    st.set_page_config(
        page_title="AI Resume Screener",
        page_icon="📄",
        layout="wide",
    )

    inject_theme()

    st.markdown(
        """
        <div class="hero-eyebrow">AI Resume Intelligence</div>
        <h1 class="hero-title">The Reviewer's Desk</h1>
        <p class="hero-sub">
            Upload resumes, paste a job description, and get a scored,
            evidence-based read on every candidate — keyword match, meaning-level
            fit, and an AI second opinion on what to fix.
        </p>
        <hr class="hairline-rule" />
        """,
        unsafe_allow_html=True,
    )
