"""
LLM-powered cover letter generation.

Plain-text output (not JSON) since a cover letter is meant to be read/copied
as-is. Grounded in the actual resume content so it doesn't invent experience.
"""

import streamlit as st

from config import GEMINI_MODEL
from llm.gemini_client import get_client

SYSTEM_INSTRUCTION = """You are an expert cover letter writer. You write concise, \
specific, non-generic cover letters grounded ONLY in the candidate's actual resume \
content — never invent employers, projects, skills, or achievements that aren't in \
the resume. Avoid cliches like "I am writing to express my interest" and "team player" \
filler. Open with something specific to the role or company. Keep it to 3-4 short \
paragraphs. Output ONLY the cover letter body text — no subject line, no markdown, \
no commentary, no placeholder brackets left unfilled (if a detail like company name \
is missing, write around it naturally instead of leaving a [BRACKET])."""


def _build_prompt(resume_text: str, jd_text: str, applicant_name: str,
                   company_name: str, hiring_manager: str, tone: str) -> str:
    greeting = f"Dear {hiring_manager}," if hiring_manager.strip() else "Dear Hiring Manager,"
    company_line = f"The company is: {company_name}." if company_name.strip() else "Company name was not provided — do not guess one."
    name_line = f"Sign off as: {applicant_name}." if applicant_name.strip() else "Sign off as: [Your Name] — the user will fill this in."

    return f"""JOB DESCRIPTION:
{jd_text}

CANDIDATE'S RESUME:
{resume_text}

DETAILS:
- Tone: {tone}
- Greeting to use: {greeting}
- {company_line}
- {name_line}

Write the complete cover letter now, grounded only in what's in the resume above.
"""


@st.cache_data(show_spinner=False)
def generate_cover_letter(
    resume_text: str,
    jd_text: str,
    applicant_name: str,
    company_name: str,
    hiring_manager: str,
    tone: str,
) -> str:
    """Returns the cover letter text, or a string starting with 'ERROR:' on failure."""
    client = get_client()
    if client is None:
        return "ERROR: No Gemini API key configured. Add one in the sidebar to use this feature."

    prompt = _build_prompt(resume_text, jd_text, applicant_name, company_name, hiring_manager, tone)

    try:
        from google.genai import types

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.6,
            ),
        )
        return response.text.strip()

    except Exception as exc:
        return f"ERROR: Cover letter generation failed: {exc}"
