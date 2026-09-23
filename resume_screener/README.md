# AI Resume Screener

TF-IDF + semantic (local embeddings) resume-to-JD matching, with optional
Gemini-powered ATS gap analysis.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Gemini API key (free tier)

1. Get a free key at https://aistudio.google.com/apikey
2. Either:
   - Copy `.env.example` to `.env` and fill in `GEMINI_API_KEY`, or
   - Export it: `export GEMINI_API_KEY=your_key` (Linux/Mac) / `set GEMINI_API_KEY=your_key` (Windows), or
   - Paste it into the sidebar text box when the app is running (session-only, not saved)

## Run

```bash
streamlit run app.py
```

## AI Features (per resume, opt-in)

-  Gap Analysis — explains why the match score is what it is, lists
  strengths/gaps, and gives prioritized fixes.
-  Resume Optimizer — rewrites the 3-5 weakest bullets and suggests a
  tailored professional summary. Grounded only in what's already in the
  resume — it's instructed not to invent skills, employers, or metrics.
-  Cover Letter Generator — drafts a tailored cover letter (name/company/
  hiring manager/tone are optional inputs), downloadable as `.txt`.

Each is a separate button/tab per resume so nothing runs automatically —
you control exactly when API calls happen.

## Theme

Dark editorial theme ("The Reviewer's Desk") in `ui/theme.py` and
`.streamlit/config.toml` — ink background, brass accent, serif headlines,
monospace data/scores, and a circular "verdict stamp" badge for match scores.
No new dependencies; fonts load from Google Fonts at runtime. To adjust
colors, edit the `:root` variables at the top of `ui/theme.py`.

## Notes

- First run downloads the spaCy model and the sentence-transformer model —
  this is one-time and cached after that (`st.cache_resource`).
- The `google-genai` SDK and `gemini-2.5-flash` model name are current as of
  this writing — if Google renames/deprecates either, only `llm/gemini_client.py`
  and `config.py` need updates, nothing else.
- AI gap analysis is opt-in per resume (button click) to avoid burning free-tier
  quota automatically on every upload.

## What was fixed from the original single-file version

- Substring skill-matching bug: `"java" in "javascript"` was `True`, so any
  resume mentioning only JavaScript was wrongly credited with knowing Java.
  Fixed with word-boundary regex matching.
- No caching: spaCy/NLTK were reloaded from disk on every Streamlit rerun
  (every click), causing multi-second lag. Now cached with `st.cache_resource`.
- No PDF error handling: corrupted or scanned/image-only PDFs silently
  produced empty text, which crashed TF-IDF downstream with a cryptic error.
  Now caught and surfaced as a clear per-file warning, and the rest of the
  batch still runs.
- TF-IDF-only matching: added local semantic embeddings so resumes that
  are relevant but phrased differently from the JD aren't missed.
