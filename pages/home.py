import streamlit as st

def render():
    """Renders the landing page for HireLens."""
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 40px 0 20px 0;'>
        <div style='display: inline-block; background: rgba(79, 140, 255, 0.12); color: #4F8CFF; border: 1px solid rgba(79, 140, 255, 0.3); border-radius: 20px; padding: 6px 18px; font-size: 14px; font-weight: 700; margin-bottom: 16px;'>
            ✨ NEXT-GEN AI CAREER PLATFORM
        </div>
        <h1 style='font-size: 3.4rem; font-weight: 800; background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px;'>
            HireLens
        </h1>
        <h3 style='font-size: 1.5rem; color: #38BDF8; font-weight: 600; margin-bottom: 24px;'>
            “See your resume through the eyes of recruiters.”
        </h3>
        <p style='font-size: 1.1rem; color: #94A3B8; max-width: 720px; margin: 0 auto 36px auto; line-height: 1.6;'>
            Analyze your resume against any job description in seconds. Uncover ATS compatibility scores, identify critical skill gaps, leverage semantic AI matching, and receive actionable recruiter-grade optimization recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Analyze My Resume Now", key="hero_btn_analyze"):
            st.session_state.current_page = "analyzer"
            st.rerun()

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08); margin: 40px 0;'><br>", unsafe_allow_html=True)

    # Features Section Header
    st.markdown("<h2 style='text-align: center; margin-bottom: 32px;'>Built for Jobseekers & Career Growth</h2>", unsafe_allow_html=True)

    fcol1, fcol2 = st.columns(2)

    with fcol1:
        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">📄</div>
            <h3 style="margin-bottom: 8px;">Smart Resume Parsing</h3>
            <p style="color: #94A3B8;">Automatically parse PDF resumes using PyMuPDF to extract technical skills, experience spans, education, and project blocks with zero data loss.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">🧠</div>
            <h3 style="margin-bottom: 8px;">Semantic AI Matching</h3>
            <p style="color: #94A3B8;">Beyond exact keywords. Our semantic engine measures contextual relevance between your achievements and target job requirements.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">💡</div>
            <h3 style="margin-bottom: 8px;">AI Optimization Tips</h3>
            <p style="color: #94A3B8;">Receive personalized, non-misleading advice to format bullet points, quantify results, and highlight target competencies effectively.</p>
        </div>
        """, unsafe_allow_html=True)

    with fcol2:
        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">🎯</div>
            <h3 style="margin-bottom: 8px;">Weighted ATS Compatibility</h3>
            <p style="color: #94A3B8;">Get a multi-factor score breakdown (Skills, Semantic, Keyword, Experience, Education) that reflects real-world ATS filtering criteria.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">📊</div>
            <h3 style="margin-bottom: 8px;">Career Analytics Dashboard</h3>
            <p style="color: #94A3B8;">Track your ATS score progress over time, visualize skill match distributions with Plotly graphs, and compare past analyses.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hirelens-card">
            <div style="font-size: 28px; margin-bottom: 12px;">💼</div>
            <h3 style="margin-bottom: 8px;">Multi-Job Match Comparison</h3>
            <p style="color: #94A3B8;">"Which job fits me best?" Compare your single resume against multiple job descriptions to target roles where you have highest fit.</p>
        </div>
        """, unsafe_allow_html=True)
