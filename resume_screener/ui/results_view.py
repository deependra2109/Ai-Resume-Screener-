import pandas as pd
import streamlit as st

from llm.ats_analysis import get_ats_gap_analysis
from llm.resume_optimizer import get_resume_optimization
from llm.cover_letter import generate_cover_letter
from llm.gemini_client import has_api_key
from ui.theme import verdict_stamp_html, chip_row_html


def render_results(resume_results: list[dict], jd_skills_count: int, raw_jd: str):
    if not resume_results:
        st.warning("No resumes could be scored. Check the errors above.")
        return

    resume_results = sorted(resume_results, key=lambda x: x["blended"], reverse=True)

    st.subheader("📊 Overall Results")
    best = resume_results[0]
    c1, c2, c3 = st.columns([1, 2, 2])
    with c1:
        st.markdown(verdict_stamp_html(best["blended"] * 100), unsafe_allow_html=True)
    with c2:
        st.metric("Top Candidate", best["Resume File"])
    with c3:
        st.metric("JD Skills Count", jd_skills_count)

    st.markdown("### 🧾 Detailed Table")
    table_df = pd.DataFrame(
        [
            {
                "Resume File": r["Resume File"],
                "Blended Match %": round(r["blended"] * 100, 1),
                "Keyword (TF-IDF) %": round(r["tfidf"] * 100, 1),
                "Semantic %": round(r["semantic"] * 100, 1),
                "Matched Skills": r["Matched Skills"],
                "Missing Skills": r["Missing Skills"],
            }
            for r in resume_results
        ]
    )
    st.dataframe(table_df, use_container_width=True, hide_index=True)

    st.markdown("### 🔍 Per-Resume Details")
    for res in resume_results:
        with st.expander(f"📄 {res['Resume File']} — {res['blended'] * 100:.1f}% match"):
            _render_resume_detail(res, raw_jd)

    st.success("✅ Analysis complete!")


def _render_resume_detail(res: dict, raw_jd: str):
    fname = res["Resume File"]

    stamp_col, metrics_col = st.columns([1, 4])
    with stamp_col:
        st.markdown(verdict_stamp_html(res["blended"] * 100), unsafe_allow_html=True)
    with metrics_col:
        col1, col2 = st.columns(2)
        col1.metric("Keyword", f"{res['tfidf'] * 100:.1f}%")
        col2.metric("Semantic", f"{res['semantic'] * 100:.1f}%")

    tab_skills, tab_gap, tab_optimize, tab_cover = st.tabs(
        ["Skills", "🤖 Gap Analysis", "✍️ Resume Optimizer", "📨 Cover Letter"]
    )

    with tab_skills:
        st.caption("✅ Matched Skills")
        st.markdown(chip_row_html(sorted(res["_matched_skills"]), "good"), unsafe_allow_html=True)
        st.caption("⚠️ Missing Skills")
        st.markdown(chip_row_html(sorted(res["_missing_skills"]), "gap"), unsafe_allow_html=True)

    if not has_api_key():
        for tab in (tab_gap, tab_optimize, tab_cover):
            with tab:
                st.info("Add a Gemini API key in the sidebar to enable this.")
        return

    with tab_gap:
        _render_gap_analysis_tab(res, raw_jd, fname)

    with tab_optimize:
        _render_optimizer_tab(res, raw_jd, fname)

    with tab_cover:
        _render_cover_letter_tab(res, raw_jd, fname)


def _render_gap_analysis_tab(res: dict, raw_jd: str, fname: str):
    if st.button("Get AI Gap Analysis", key=f"gap_btn_{fname}"):
        with st.spinner("Asking Gemini for a detailed breakdown..."):
            result = get_ats_gap_analysis(
                resume_text=res["_raw_text"],
                jd_text=raw_jd,
                matched_skills=tuple(sorted(res["_matched_skills"])),
                missing_skills=tuple(sorted(res["_missing_skills"])),
                score_pct=res["blended"] * 100,
            )
        st.session_state[f"gap_result_{fname}"] = result

    result = st.session_state.get(f"gap_result_{fname}")
    if not result:
        return
    if "error" in result:
        st.error(result["error"])
        return

    st.write(f"**Verdict:** {result.get('verdict', '-')}")
    st.write(result.get("score_explanation", ""))

    if result.get("strengths"):
        st.write("**Strengths:**")
        for s in result["strengths"]:
            st.write(f"- {s}")

    if result.get("gaps"):
        st.write("**Gaps:**")
        for g in result["gaps"]:
            st.write(f"- {g}")

    if result.get("prioritized_actions"):
        st.write("**Prioritized Actions:**")
        for i, a in enumerate(result["prioritized_actions"], 1):
            st.write(f"{i}. {a}")


def _render_optimizer_tab(res: dict, raw_jd: str, fname: str):
    st.caption("Rewrites are grounded in your actual resume content — it won't invent skills or experience.")

    if st.button("Optimize Resume for This JD", key=f"opt_btn_{fname}"):
        with st.spinner("Asking Gemini to rewrite the weakest sections..."):
            result = get_resume_optimization(
                resume_text=res["_raw_text"],
                jd_text=raw_jd,
                missing_skills=tuple(sorted(res["_missing_skills"])),
                matched_skills=tuple(sorted(res["_matched_skills"])),
            )
        st.session_state[f"opt_result_{fname}"] = result

    result = st.session_state.get(f"opt_result_{fname}")
    if not result:
        return
    if "error" in result:
        st.error(result["error"])
        return

    if result.get("professional_summary_rewrite"):
        st.write("**Suggested Professional Summary:**")
        st.info(result["professional_summary_rewrite"])

    if result.get("bullet_rewrites"):
        st.write("**Bullet Rewrites:**")
        for b in result["bullet_rewrites"]:
            st.markdown(f"~~{b.get('original', '')}~~")
            st.write(f"→ {b.get('improved', '')}")
            st.caption(b.get("why", ""))
            st.markdown("---")

    if result.get("keywords_to_naturally_add"):
        st.write("**Keywords to naturally work in (only if true):**")
        st.write(", ".join(result["keywords_to_naturally_add"]))

    if result.get("honesty_note"):
        st.warning(result["honesty_note"])


def _render_cover_letter_tab(res: dict, raw_jd: str, fname: str):
    c1, c2 = st.columns(2)
    with c1:
        applicant_name = st.text_input("Your name", key=f"cl_name_{fname}")
        company_name = st.text_input("Company name (optional)", key=f"cl_company_{fname}")
    with c2:
        hiring_manager = st.text_input("Hiring manager name (optional)", key=f"cl_manager_{fname}")
        tone = st.selectbox(
            "Tone", ["Professional", "Enthusiastic", "Concise", "Confident"], key=f"cl_tone_{fname}"
        )

    if st.button("Generate Cover Letter", key=f"cl_btn_{fname}"):
        with st.spinner("Asking Gemini to draft the cover letter..."):
            letter = generate_cover_letter(
                resume_text=res["_raw_text"],
                jd_text=raw_jd,
                applicant_name=applicant_name,
                company_name=company_name,
                hiring_manager=hiring_manager,
                tone=tone,
            )
        st.session_state[f"cl_result_{fname}"] = letter

    letter = st.session_state.get(f"cl_result_{fname}")
    if not letter:
        return
    if letter.startswith("ERROR:"):
        st.error(letter)
        return

    st.text_area("Cover Letter", value=letter, height=350, key=f"cl_display_{fname}")
    st.download_button(
        "Download as .txt",
        data=letter,
        file_name=f"cover_letter_{fname.replace('.pdf', '')}.txt",
        key=f"cl_download_{fname}",
    )
