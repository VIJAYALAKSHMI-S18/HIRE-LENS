import streamlit as st

def render():
    """Renders the landing page for HireLens."""

    dark_mode = st.session_state.get("dark_mode", True)

    # Theme-adaptive color tokens
    if dark_mode:
        h1_color        = "#FFFFFF"
        tagline_color   = "#38BDF8"
        body_color      = "#94A3B8"
        card_desc_color = "#94A3B8"
        hr_color        = "rgba(255,255,255,0.08)"
    else:
        h1_color        = "#0F172A"
        tagline_color   = "#0284C7"
        body_color      = "#475569"
        card_desc_color = "#475569"
        hr_color        = "rgba(0,0,0,0.10)"

    # Hero Section — solid color heading avoids broken gradient-clip in Streamlit iframe
    st.markdown(f"""
    <div style='text-align: center; padding: 48px 0 8px 0;'>
        <div style='display: inline-block; background: rgba(79, 140, 255, 0.12); color: #4F8CFF;
                    border: 1px solid rgba(79, 140, 255, 0.3); border-radius: 20px;
                    padding: 6px 18px; font-size: 13px; font-weight: 700;
                    margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;'>
            ✨ NEXT-GEN AI CAREER PLATFORM
        </div>
        <h1 style='font-size: 3.6rem; font-weight: 800; color: {h1_color};
                   margin: 0 0 14px 0; text-transform: uppercase; letter-spacing: 4px;'>
            HIRELENS
        </h1>
        <h3 style='font-size: 1.35rem; color: {tagline_color}; font-weight: 600;
                   margin: 0 0 22px 0; text-transform: uppercase;'>
            "SEE YOUR RESUME THROUGH THE EYES OF RECRUITERS."
        </h3>
        <p style='font-size: 1rem; color: {body_color}; max-width: 640px;
                  margin: 0 auto 36px auto; line-height: 1.7; text-transform: uppercase;'>
            ANALYZE YOUR RESUME AGAINST ANY JOB DESCRIPTION IN SECONDS.
            UNCOVER ATS COMPATIBILITY SCORES, IDENTIFY CRITICAL SKILL GAPS,
            LEVERAGE SEMANTIC AI MATCHING, AND RECEIVE RECRUITER-GRADE RECOMMENDATIONS.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Centered CTA button
    col_l, col_c, col_r = st.columns([1.6, 1, 1.6])
    with col_c:
        if st.button("🚀 ANALYZE MY RESUME NOW", key="hero_btn_analyze"):
            st.session_state.current_page = "analyzer"
            st.rerun()

    st.markdown(f"<br><hr style='border-color: {hr_color}; margin: 40px 0;'><br>", unsafe_allow_html=True)

    # Features Section
    st.markdown("<h2 style='text-align: center; margin-bottom: 32px; text-transform: uppercase;'>BUILT FOR JOBSEEKERS &amp; CAREER GROWTH</h2>", unsafe_allow_html=True)

    features = [
        ("📄", "SMART RESUME PARSING",
         "AUTOMATICALLY PARSE PDF RESUMES USING PYMUPDF TO EXTRACT TECHNICAL SKILLS, EXPERIENCE SPANS, EDUCATION, AND PROJECT BLOCKS WITH ZERO DATA LOSS."),
        ("🎯", "WEIGHTED ATS COMPATIBILITY",
         "GET A MULTI-FACTOR SCORE BREAKDOWN (SKILLS, SEMANTIC, KEYWORD, EXPERIENCE, EDUCATION) THAT REFLECTS REAL-WORLD ATS FILTERING CRITERIA."),
        ("🧠", "SEMANTIC AI MATCHING",
         "BEYOND EXACT KEYWORDS. OUR SEMANTIC ENGINE MEASURES CONTEXTUAL RELEVANCE BETWEEN YOUR ACHIEVEMENTS AND TARGET JOB REQUIREMENTS."),
        ("📊", "CAREER ANALYTICS DASHBOARD",
         "TRACK YOUR ATS SCORE PROGRESS OVER TIME, VISUALIZE SKILL MATCH DISTRIBUTIONS WITH PLOTLY GRAPHS, AND COMPARE PAST ANALYSES."),
        ("✨", "AI BULLET REWRITER",
         "TURN WEAK RESUME BULLETS INTO CLEAR, IMPACTFUL ACHIEVEMENTS WITH 6 REWRITE MODES — WITHOUT FABRICATING EXPERIENCE OR FAKE METRICS."),
        ("👁", "6-SECOND RECRUITER SKIM",
         "SIMULATE WHAT A RECRUITER LIKELY SPOTS IN THEIR FIRST GLANCE AND GET A FIRST-IMPRESSION SCORE WITH ACTIONABLE VISUAL FEEDBACK."),
        ("💼", "MULTI-JOB MATCH COMPARISON",
         "COMPARE YOUR RESUME AGAINST MULTIPLE JOB DESCRIPTIONS TO DISCOVER WHICH ROLE YOU FIT BEST AND WHERE TO FOCUS YOUR SEARCH."),
        ("📈", "RESUME A/B TESTING",
         "UPLOAD TWO RESUME VERSIONS AND COMPARE THEM SIDE-BY-SIDE AGAINST THE SAME JOB DESCRIPTION — SEE EXACTLY WHICH VERSION WINS."),
        ("💡", "AI OPTIMIZATION TIPS",
         "RECEIVE PERSONALIZED ADVICE TO FORMAT BULLET POINTS, HIGHLIGHT TARGET COMPETENCIES, AND CLOSE IDENTIFIED SKILL GAPS EFFECTIVELY."),
    ]

    # 3-column even grid
    for i in range(0, len(features), 3):
        row_features = features[i:i+3]
        cols = st.columns(len(row_features))
        for col, (icon, title, desc) in zip(cols, row_features):
            with col:
                st.markdown(f"""
                <div class="hirelens-card" style="height: 100%; min-height: 170px;">
                    <div style="font-size: 26px; margin-bottom: 10px;">{icon}</div>
                    <h3 style="margin: 0 0 8px 0; font-size: 0.9rem; text-transform: uppercase;
                               letter-spacing: 0.5px;">{title}</h3>
                    <p style="color: {card_desc_color}; font-size: 0.82rem; line-height: 1.55;
                              text-transform: uppercase; margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
