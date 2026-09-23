"""
LLM-powered ATS score explanation / gap analysis.

Given a resume, the JD, and the computed match score/skills, asks Gemini to
explain in plain English *why* the candidate scored what they did, and what
specifically to fix — going beyond the raw keyword list into things like
weak phrasing, missing quantification, and structural issues.
"""

import json
import streamlit as st

from config import GEMINI_MODEL
from llm.gemini_client import get_client

SYSTEM_INSTRUCTION = """You are an expert technical recruiter and ATS (Applicant \
Tracking System) specialist. You review a resume against a job description and \
explain the match score in a way that is specific, honest, and actionable. \
Do not be generically encouraging — be precise about real gaps. \
Always respond with ONLY valid JSON matching the exact schema given, no markdown \
fences, no extra commentary."""

RESPONSE_SCHEMA_HINT = {
    "verdict": "one short sentence, plain English, on overall fit",
    "score_explanation": "2-3 sentences on why the numeric score is what it is",
    "strengths": ["list of specific strengths relative to this JD, max 5"],
    "gaps": ["list of specific, concrete gaps relative to this JD, max 5"],
    "prioritized_actions": [
        "ordered list of the highest-impact resume changes to make, max 5, most important first"
    ],
}


def _build_prompt(resume_text: str, jd_text: str, matched_skills, missing_skills, score_pct: float) -> str:
    return f"""JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

COMPUTED DATA (from a separate similarity engine, treat as ground truth signal):
- Overall match score: {score_pct:.1f}%
- Keyword skills matched: {", ".join(sorted(matched_skills)) or "none"}
- Keyword skills missing: {", ".join(sorted(missing_skills)) or "none"}

Respond with ONLY a JSON object matching exactly this shape:
{json.dumps(RESPONSE_SCHEMA_HINT, indent=2)}
"""


@st.cache_data(show_spinner=False)
def get_ats_gap_analysis(
    resume_text: str,
    jd_text: str,
    matched_skills: tuple,
    missing_skills: tuple,
    score_pct: float,
) -> dict:
    """
    Returns a dict with keys: verdict, score_explanation, strengths, gaps,
    prioritized_actions. On failure, returns a dict with an "error" key instead.

    Cached per unique (resume, jd, skills, score) combination so re-opening an
    expander doesn't re-spend API quota.
    """
    client = get_client()
    if client is None:
        return {"error": "No Gemini API key configured. Add one in the sidebar to use AI analysis."}

    prompt = _build_prompt(resume_text, jd_text, matched_skills, missing_skills, score_pct)

    try:
        from google.genai import types

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        parsed = json.loads(response.text)
        return parsed

    except json.JSONDecodeError:
        return {"error": "AI returned an unexpected format. Try again."}
    except Exception as exc:
        return {"error": f"AI analysis failed: {exc}"}
