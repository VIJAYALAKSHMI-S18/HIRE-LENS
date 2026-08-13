import streamlit as st
from utils.bullet_rewriter import rewrite_bullet_point, REWRITE_MODES

def render():
    st.markdown("<h2 style='text-transform: uppercase;'>✨ AI BULLET POINT REWRITER</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; text-transform: uppercase;'>TURN WEAK RESUME BULLETS INTO CLEAR, IMPACTFUL, JOB-RELEVANT ACHIEVEMENTS WITHOUT FABRICATING UNVERIFIED METRICS OR EXPERIENCE.</p>", unsafe_allow_html=True)

    # Check for context from recent analysis
    last_analysis = st.session_state.get("last_analysis")
    job_desc = ""
    resume_skills = []
    
    if last_analysis:
        matched = last_analysis.get("matched_skills", [])
        missing = last_analysis.get("missing_skills", [])
        resume_skills = matched + last_analysis.get("additional_skills", [])
        st.info(f"💡 USING TARGET JOB CONTEXT FROM RECENT ANALYSIS: **{last_analysis.get('job_title', 'TARGET POSITION').upper()}**")

    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-transform: uppercase;'>SELECT OR ENTER RESUME BULLET POINT</h3>", unsafe_allow_html=True)
    
    preset_bullets = [
        "Select a pre-filled sample bullet or enter custom text below...",
        "Responsible for testing the application.",
        "Worked on a machine learning project.",
        "Created a project using Python.",
        "Helped with customer support and bug fixes.",
        "Managed database queries and SQL tables."
    ]
    
    selected_sample = st.selectbox("SAMPLE BULLET SUGGESTIONS", preset_bullets, index=1, key="rewriter_sample_select")
    
    initial_text = selected_sample if selected_sample != preset_bullets[0] else "Responsible for testing the application."
    
    input_bullet = st.text_area(
        "ORIGINAL BULLET POINT",
        value=initial_text,
        height=100,
        placeholder="Enter your resume bullet point here (e.g. Responsible for testing the application)...",
        key="rewriter_bullet_input"
    )

    col_mode, col_btn = st.columns([2, 1])
    
    with col_mode:
        selected_mode = st.selectbox(
            "REWRITE STYLE / IMPROVEMENT TYPE",
            REWRITE_MODES,
            index=0,
            key="rewriter_mode_select"
        )

    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        run_rewrite = st.button("✨ REWRITE BULLET", key="btn_run_rewrite")

    st.markdown("</div>", unsafe_allow_html=True)

    if run_rewrite:
        if not input_bullet.strip():
            st.error("PLEASE ENTER A BULLET POINT TO REWRITE.")
            return

        with st.spinner("RUNNING RECRUITER AI BULLET ENHANCER..."):
            result = rewrite_bullet_point(
                original_bullet=input_bullet,
                mode=selected_mode,
                job_description=job_desc,
                resume_skills=resume_skills
            )
            st.session_state["bullet_rewrite_result"] = result

    if "bullet_rewrite_result" in st.session_state:
        res = st.session_state["bullet_rewrite_result"]
        
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>REWRITE COMPARISON</h3>", unsafe_allow_html=True)

        res_col1, res_col2 = st.columns(2)

        with res_col1:
            st.markdown("""
            <div class='hirelens-card' style='border-left: 4px solid #94A3B8;'>
                <div style='font-size: 0.85rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;'>
                    🔴 ORIGINAL BULLET
                </div>
                <div style='font-size: 1.1rem; color: #F8FAFC; line-height: 1.6;'>
                    "{original}"
                </div>
            </div>
            """.format(original=res['original']), unsafe_allow_html=True)

        with res_col2:
            st.markdown("""
            <div class='hirelens-card' style='border-left: 4px solid #38BDF8; background: rgba(56, 189, 248, 0.08);'>
                <div style='font-size: 0.85rem; color: #38BDF8; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;'>
                    ✨ AI IMPROVED ({mode})
                </div>
                <div style='font-size: 1.15rem; font-weight: 600; color: #38BDF8; line-height: 1.6;'>
                    "{improved}"
                </div>
            </div>
            """.format(improved=res['improved'], mode=res['mode'].upper()), unsafe_allow_html=True)

        # Action Buttons
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            if st.button("📋 COPY IMPROVED BULLET", key="btn_copy_bullet"):
                st.toast("COPIED IMPROVED BULLET TO CLIPBOARD!", icon="✅")
        with b_col2:
            if st.button("🔄 REGENERATE", key="btn_regen_bullet"):
                with st.spinner("REGENERATING..."):
                    new_res = rewrite_bullet_point(
                        original_bullet=res['original'],
                        mode=res['mode'],
                        job_description=job_desc,
                        resume_skills=resume_skills
                    )
                    st.session_state["bullet_rewrite_result"] = new_res
                    st.rerun()
        with b_col3:
            if st.button("↩ USE ORIGINAL", key="btn_use_orig"):
                st.session_state["bullet_rewrite_result"] = {
                    "original": res['original'],
                    "improved": res['original'],
                    "mode": "Original",
                    "reasons": ["Kept original phrasing."]
                }
                st.rerun()

        # Explanation Box
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-transform: uppercase; color: #38BDF8;'>💡 WHY THIS IS BETTER</h4>", unsafe_allow_html=True)
        for r in res.get("reasons", []):
            st.markdown(f"• **{r}**")
        st.markdown("<p style='font-size: 0.85rem; color: #94A3B8; margin-top: 12px;'>🛡️ <strong>HONESTY GUARANTEE:</strong> HireLens improves action verb strength and structural impact without fabricating unverified metrics or achievements.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
