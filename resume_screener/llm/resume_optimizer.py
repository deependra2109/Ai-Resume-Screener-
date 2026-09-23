"""
LLM-powered resume optimization/rewrite.

Given a resume and a JD, asks Gemini to rewrite the weakest parts of the resume
so it's more tailored to that specific JD — not a generic "make it better",
but targeted at the actual gaps between this resume and this job.
"""

import json
import streamlit as st

from config import GEMINI_MODEL
from llm.gemini_client import get_client

SYSTEM_INSTRUCTION = """You are an expert resume writer who specializes in tailoring \
resumes to specific job descriptions for ATS and human reviewers. You rewrite \
based on what is ALREADY TRUE in the candidate's resume — you elaborate, \
quantify, and rephrase using stronger action verbs and JD-relevant language, \
but you NEVER invent skills, employers, metrics, or experience that aren't \
supported by the original resume. If a bullet is genuinely too thin to improve \
honestly, say so instead of fabricating detail. \
Always respond with ONLY valid JSON matching the exact schema given, no markdown \
fences, no extra commentary."""

RESPONSE_SCHEMA_HINT = {
    "professional_summary_rewrite": "a 2-3 sentence professional summary tailored to this JD, based only on what's in the resume",
    "bullet_rewrites": [
        {
            "original": "the original bullet/line from the resume, verbatim",
            "improved": "the rewritten version — stronger verb, quantified where honestly possible, JD-aligned phrasing",
            "why": "one short sentence on what changed and why",
        }
    ],
    "keywords_to_naturally_add": [
        "JD keywords/phrases missing from the resume that the candidate could honestly add if true, max 8"
    ],
    "honesty_note": "any caveat about claims that should NOT be added without being true, or empty string if none",
}


def _build_prompt(resume_text: str, jd_text: str, missing_skills, matched_skills) -> str:
    return f"""JOB DESCRIPTION:
{jd_text}

CURRENT RESUME:
{resume_text}

CONTEXT:
- Skills already matched to this JD: {", ".join(sorted(matched_skills)) or "none"}
- Skills the JD wants but the resume doesn't mention: {", ".join(sorted(missing_skills)) or "none"}

Pick the 3-5 weakest or least JD-relevant bullets in the resume and rewrite them.
Respond with ONLY a JSON object matching exactly this shape:
{json.dumps(RESPONSE_SCHEMA_HINT, indent=2)}
"""


@st.cache_data(show_spinner=False)
def get_resume_optimization(
    resume_text: str,
    jd_text: str,
    missing_skills: tuple,
    matched_skills: tuple,
) -> dict:
    """
    Returns a dict with keys: professional_summary_rewrite, bullet_rewrites,
    keywords_to_naturally_add, honesty_note. On failure, returns {"error": ...}.
    """
    client = get_client()
    if client is None:
        return {"error": "No Gemini API key configured. Add one in the sidebar to use AI optimization."}

    prompt = _build_prompt(resume_text, jd_text, missing_skills, matched_skills)

    try:
        from google.genai import types

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.4,
            ),
        )
        return json.loads(response.text)

    except json.JSONDecodeError:
        return {"error": "AI returned an unexpected format. Try again."}
    except Exception as exc:
        return {"error": f"AI optimization failed: {exc}"}
