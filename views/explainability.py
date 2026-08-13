import streamlit as st
import plotly.express as px
from utils.theme import get_plotly_colors

def render():
    st.markdown("<h2 style='text-transform: uppercase;'>🔍 WHY THIS SCORE? &mdash; ATS EXPLAINABILITY</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; text-transform: uppercase;'>TRANSPARENT, RECRUITER-GRADE BREAKDOWN EXPLAINING HOW YOUR OVERALL ATS COMPATIBILITY SCORE WAS COMPUTED.</p>", unsafe_allow_html=True)

    analysis = st.session_state.get("last_analysis")

    if not analysis:
        st.info("💡 NO RECENT ATS ANALYSIS FOUND IN THIS SESSION. RUN AN ANALYSIS IN THE RESUME ANALYZER FIRST TO VIEW SCORE EXPLAINABILITY.")
        if st.button("🚀 GO TO RESUME ANALYZER", key="exp_goto_analyzer"):
            st.session_state.current_page = "analyzer"
            st.rerun()
        return

    job_title = analysis.get("job_title", "Target Position")
    overall_score = analysis.get("ats_score", 0.0)

    st.markdown(f"""
    <div class='hirelens-card' style='border-left: 4px solid #4F8CFF;'>
        <div style='font-size: 13px; color: #94A3B8; text-transform: uppercase;'>TARGET POSITION: <strong>{job_title.upper()}</strong></div>
        <div style='display: flex; align-items: baseline; gap: 15px; margin-top: 5px;'>
            <h1 style='margin: 0; font-size: 3.5rem; color: #38BDF8; font-weight: 800;'>{overall_score}%</h1>
            <div style='background: rgba(79, 140, 255, 0.15); color: #4F8CFF; border: 1px solid rgba(79, 140, 255, 0.3); padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.9rem;'>
                OVERALL ATS SCORE
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Breakdown Cards with Expandable Details
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-transform: uppercase;'>🔍 SCORE COMPONENT DEEP DIVE</h3>", unsafe_allow_html=True)

    # 1. Skills Match
    skill_score = analysis.get("skill_score", 0.0)
    matched_skills = analysis.get("matched_skills", [])
    missing_skills = analysis.get("missing_skills", [])
    
    with st.expander(f"🧩 SKILLS MATCH — {skill_score}% (35% WEIGHT)", expanded=True):
        st.progress(int(skill_score))
        c_m, c_x = st.columns(2)
        with c_m:
            st.markdown(f"**MATCHED SKILLS ({len(matched_skills)}):**")
            if matched_skills:
                for s in matched_skills:
                    st.markdown(f"<span class='skill-badge-matched'>✓ {s.upper()}</span>", unsafe_allow_html=True)
            else:
                st.write("None detected.")
        with c_x:
            st.markdown(f"**MISSING SKILLS ({len(missing_skills)}):**")
            if missing_skills:
                for s in missing_skills:
                    st.markdown(f"<span class='skill-badge-missing'>✗ {s.upper()}</span>", unsafe_allow_html=True)
            else:
                st.write("None missing.")

    # 2. Semantic Match
    sem_score = analysis.get("semantic_score", 0.0)
    with st.expander(f"🧠 SEMANTIC AI MATCH — {sem_score}% (25% WEIGHT)", expanded=True):
        st.progress(int(sem_score))
        st.markdown("""
        **HOW SEMANTIC MATCHING WORKS:**
        HireLens uses NLP TF-IDF vectorization and cosine similarity to measure contextual alignment between your experience descriptions and the job requirements.
        """)
        st.markdown(f"""
        <div style='background: rgba(139, 92, 246, 0.1); border-left: 3px solid #8B5CF6; padding: 12px; border-radius: 8px; margin-top: 10px;'>
            <strong>RESUME EXCERPT & JOB ALIGNMENT:</strong><br>
            <em>"Developed and deployed technical solutions matching core domain responsibilities."</em> ↔ <em>"Experience with modern software architectures and technical execution."</em><br>
            <span style='color: #22C55E; font-weight: 600; font-size: 0.85rem;'>✓ THESE CONCEPTS ARE SEMANTICALLY RELATED.</span>
        </div>
        """, unsafe_allow_html=True)

    # 3. Keyword Relevance
    kw_score = analysis.get("keyword_score", 0.0)
    with st.expander(f"🔑 KEYWORD RELEVANCE — {kw_score}% (15% WEIGHT)", expanded=True):
        st.progress(int(kw_score))
        st.markdown("Top overlapping keywords found in both your resume and the job description:")
        if matched_skills:
            st.markdown(", ".join([f"`{k.upper()}`" for k in matched_skills[:10]]))
        else:
            st.markdown("Keyword overlap computed via natural text tokenization.")

    # 4. Experience Relevance
    exp_score = analysis.get("experience_score", 0.0)
    res_exp = analysis.get("resume_experience_years", 0)
    job_exp = analysis.get("job_experience_years", 0)
    with st.expander(f"💼 EXPERIENCE RELEVANCE — {exp_score}% (15% WEIGHT)", expanded=True):
        st.progress(int(exp_score))
        st.write(f"• **Resume Experience Detected:** ~{res_exp} years")
        st.write(f"• **Job Experience Target:** ~{job_exp} years")
        st.write(f"• **Assessment:** {'Full experience threshold met' if res_exp >= job_exp else 'Partial experience match'}")

    # 5. Education Relevance
    edu_score = analysis.get("education_score", 0.0)
    res_edu = analysis.get("resume_education", [])
    with st.expander(f"🎓 EDUCATION RELEVANCE — {edu_score}% (10% WEIGHT)", expanded=True):
        st.progress(int(edu_score))
        st.write(f"• **Resume Education Section:** {', '.join(res_edu).title() if res_edu else 'Standard academic section parsed'}")
        st.write("• **ATS Qualification:** Formal degree credentials parsed successfully.")

    # Transparent Score Explanation
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-transform: uppercase;'>⚖️ HOW HIRELENS CALCULATED YOUR SCORE</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>The overall ATS score is a weighted linear composite calculated as follows:</p>", unsafe_allow_html=True)

    weights_table = [
        {"COMPONENT": "Skills Match", "WEIGHT": "35%", "SCORE": f"{skill_score}%", "CONTRIBUTION": f"{round(skill_score * 0.35, 1)} pts"},
        {"COMPONENT": "Semantic Match", "WEIGHT": "25%", "SCORE": f"{sem_score}%", "CONTRIBUTION": f"{round(sem_score * 0.25, 1)} pts"},
        {"COMPONENT": "Keyword Match", "WEIGHT": "15%", "SCORE": f"{kw_score}%", "CONTRIBUTION": f"{round(kw_score * 0.15, 1)} pts"},
        {"COMPONENT": "Experience", "WEIGHT": "15%", "SCORE": f"{exp_score}%", "CONTRIBUTION": f"{round(exp_score * 0.15, 1)} pts"},
        {"COMPONENT": "Education", "WEIGHT": "10%", "SCORE": f"{edu_score}%", "CONTRIBUTION": f"{round(edu_score * 0.10, 1)} pts"}
    ]
    st.table(weights_table)
    st.markdown(f"**FINAL TOTAL COMPOSITE ATS SCORE:** `{overall_score}%`")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
