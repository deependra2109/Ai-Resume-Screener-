import streamlit as st
from llm.gemini_client import has_api_key


def render_sidebar():
    with st.sidebar:
        st.subheader("🔑 Gemini API Key")
        if has_api_key():
            st.success("API key detected ✅")
        else:
            st.text_input(
                "Paste your Gemini API key",
                type="password",
                key="gemini_api_key_manual",
                help="Get a free key at https://aistudio.google.com/apikey. "
                     "Stored only for this browser session, never saved to disk.",
            )
            st.caption(
                "For local/deployed use, prefer setting the GEMINI_API_KEY "
                "environment variable or Streamlit secrets instead."
            )

        st.markdown("---")
        st.subheader("ℹ️ How scoring works")
        st.write(
            """
            - **TF-IDF score** — exact keyword/phrase overlap
            - **Semantic score** — meaning-level match via local embeddings
              (catches relevant experience phrased differently than the JD)
            - **Blended score** — weighted combination of both, shown as the
              headline match %
            """
        )

        st.markdown("---")
        st.subheader("🤖 AI Features (per resume)")
        st.write(
            """
            - **Gap Analysis** — explains the score, strengths, gaps, priorities
            - **Resume Optimizer** — rewrites weak bullets + summary, grounded
              in what's actually in the resume
            - **Cover Letter** — drafts a tailored letter, downloadable as .txt
            """
        )
