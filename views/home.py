import streamlit as st

def render():
    """Renders the landing page for HireLens."""
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 40px 0 20px 0;'>
        <div style='display: inline-block; background: rgba(79, 140, 255, 0.12); color: #4F8CFF; border: 1px solid rgba(79, 140, 255, 0.3); border-radius: 20px; padding: 6px 18px; font-size: 14px; font-weight: 700; margin-bottom: 16px; text-transform: uppercase;'>
            ✨ NEXT-GEN AI CAREER PLATFORM
        </div>
        <h1 style='font-size: 3.4rem; font-weight: 800; background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; text-transform: uppercase;'>
            HIRELENS
        </h1>
        <h3 style='font-size: 1.5rem; color: #38BDF8; font-weight: 600; margin-bottom: 24px; text-transform: uppercase;'>
            “SEE YOUR RESUME THROUGH THE EYES OF RECRUITERS.”
        </h3>
        <p style='font-size: 1.1rem; color: #94A3B8; max-width: 720px; margin: 0 auto 36px auto; line-height: 1.6; text-transform: uppercase;'>
            ANALYZE YOUR RESUME AGAINST ANY JOB DESCRIPTION IN SECONDS. UNCOVER ATS COMPATIBILITY SCORES, IDENTIFY CRITICAL SKILL GAPS, LEVERAGE SEMANTIC AI MATCHING, AND RECEIVE ACTIONABLE RECRUITER-GRADE OPTIMIZATION RECOMMENDATIONS.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ANALYZE MY RESUME NOW", key="hero_btn_analyze"):
            st.session_state.current_page = "analyzer"
            st.rerun()

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08); margin: 40px 0;'><br>", unsafe_allow_html=True)

    # Features Section Header
    st.markdown("<h2 style='text-align: center; margin-bottom: 32px; text-transform: uppercase;'>BUILT FOR JOBSEEKERS & CAREER GROWTH</h2>", unsafe_allow_html=True)

    fcol1, fcol2 = st.columns(2)

    with fcol1:
        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">📄</div>
            <h3 style="margin-bottom: 8px; text-transform: uppercase;">SMART RESUME PARSING</h3>
            <p style="color: #94A3B8; text-transform: uppercase;">AUTOMATICALLY PARSE PDF RESUMES USING PYMUPDF TO EXTRACT TECHNICAL SKILLS, EXPERIENCE SPANS, EDUCATION, AND PROJECT BLOCKS WITH ZERO DATA LOSS.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">🧠</div>
            <h3 style="margin-bottom: 8px; text-transform: uppercase;">SEMANTIC AI MATCHING</h3>
            <p style="color: #94A3B8; text-transform: uppercase;">BEYOND EXACT KEYWORDS. OUR SEMANTIC ENGINE MEASURES CONTEXTUAL RELEVANCE BETWEEN YOUR ACHIEVEMENTS AND TARGET JOB REQUIREMENTS.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">💡</div>
            <h3 style="margin-bottom: 8px; text-transform: uppercase;">AI OPTIMIZATION TIPS</h3>
            <p style="color: #94A3B8; text-transform: uppercase;">RECEIVE PERSONALIZED, NON-MISLEADING ADVICE TO FORMAT BULLET POINTS, QUANTIFY RESULTS, AND HIGHLIGHT TARGET COMPETENCIES EFFECTIVELY.</p>
        </div>
        """, unsafe_allow_html=True)

    with fcol2:
        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">🎯</div>
            <h3 style="margin-bottom: 8px; text-transform: uppercase;">WEIGHTED ATS COMPATIBILITY</h3>
            <p style="color: #94A3B8; text-transform: uppercase;">GET A MULTI-FACTOR SCORE BREAKDOWN (SKILLS, SEMANTIC, KEYWORD, EXPERIENCE, EDUCATION) THAT REFLECTS REAL-WORLD ATS FILTERING CRITERIA.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">📊</div>
            <h3 style="margin-bottom: 8px; text-transform: uppercase;">CAREER ANALYTICS DASHBOARD</h3>
            <p style="color: #94A3B8; text-transform: uppercase;">TRACK YOUR ATS SCORE PROGRESS OVER TIME, VISUALIZE SKILL MATCH DISTRIBUTIONS WITH PLOTLY GRAPHS, AND COMPARE PAST ANALYSES.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">💼</div>
            <h3 style="margin-bottom: 8px; text-transform: uppercase;">MULTI-JOB MATCH COMPARISON</h3>
            <p style="color: #94A3B8; text-transform: uppercase;">"WHICH JOB FITS ME BEST?" COMPARE YOUR SINGLE RESUME AGAINST MULTIPLE JOB DESCRIPTIONS TO TARGET ROLES WHERE YOU HAVE HIGHEST FIT.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
