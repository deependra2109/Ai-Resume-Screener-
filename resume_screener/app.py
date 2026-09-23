import streamlit as st

from config import MAX_RESUMES, MAX_PDF_SIZE_MB
from core.pdf_extractor import extract_resume_text_from_file
from core.text_preprocessing import preprocess_text
from core.skill_matcher import extract_skills_from_text
from core.similarity import compute_blended_scores
from ui.styles import render_header
from ui.sidebar import render_sidebar
from ui.results_view import render_results

render_header()
render_sidebar()

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("1️⃣ Upload Resumes")
    uploaded_resumes = st.file_uploader(
        "Upload one or more resume PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        help=f"Up to {MAX_RESUMES} files, {MAX_PDF_SIZE_MB}MB each.",
    )

    st.subheader("2️⃣ Paste Job Description (JD)")
    job_description = st.text_area(
        "",
        height=220,
        placeholder=(
            "Example: We are looking for a Data Scientist with 3+ years of experience "
            "in Python, Machine Learning, SQL, and data analysis..."
        ),
    )

    analyze_button = st.button("🚀 Analyze Resumes", use_container_width=True)

with right_col:
    st.subheader("ℹ️ What this tool does")
    st.write(
        """
        - Reads each resume (PDF) and cleans the text
        - Scores match using **TF-IDF + semantic embeddings**, blended
        - Extracts **skills mentioned in the JD**, shows matched/missing per resume
        - Optional **AI gap analysis** (Gemini) explains the score and what to fix
        """
    )
    st.info("Tip: A skill-rich JD (Python, SQL, Machine Learning, AWS...) matches better.")

st.markdown("---")

if analyze_button:
    if not uploaded_resumes:
        st.error("❌ Please upload at least one resume PDF.")
    elif not job_description.strip():
        st.error("❌ Please paste a Job Description.")
    elif len(uploaded_resumes) > MAX_RESUMES:
        st.error(f"❌ Please upload at most {MAX_RESUMES} resumes at a time.")
    else:
        oversized = [f.name for f in uploaded_resumes if f.size > MAX_PDF_SIZE_MB * 1024 * 1024]
        if oversized:
            st.error(f"❌ These files exceed {MAX_PDF_SIZE_MB}MB: {', '.join(oversized)}")
        else:
            with st.spinner("Processing resumes... this may take a few seconds ⏳"):
                raw_jd = job_description
                cleaned_jd = preprocess_text(raw_jd)
                jd_skills = extract_skills_from_text(raw_jd)

                extraction_results = [extract_resume_text_from_file(f) for f in uploaded_resumes]

                failed = [r for r in extraction_results if not r.success]
                usable = [r for r in extraction_results if r.success]

                for f in failed:
                    st.warning(f"⚠️ Skipped **{f.filename}**: {f.error}")

                if not usable:
                    st.error("❌ None of the uploaded PDFs could be read. Please check the files.")
                else:
                    raw_texts = [r.text for r in usable]
                    cleaned_texts = [preprocess_text(t) for t in raw_texts]

                    scores = compute_blended_scores(cleaned_texts, cleaned_jd, raw_texts, raw_jd)

                    resume_results = []
                    for extraction, score in zip(usable, scores):
                        resume_skills = extract_skills_from_text(extraction.text)
                        matched = jd_skills & resume_skills
                        missing = jd_skills - resume_skills

                        resume_results.append({
                            "Resume File": extraction.filename,
                            "tfidf": score["tfidf"],
                            "semantic": score["semantic"],
                            "blended": score["blended"],
                            "Matched Skills": ", ".join(sorted(matched)) or "-",
                            "Missing Skills": ", ".join(sorted(missing)) or "-",
                            "_raw_text": extraction.text,
                            "_matched_skills": matched,
                            "_missing_skills": missing,
                        })

            if usable:
                render_results(resume_results, len(jd_skills), raw_jd)
