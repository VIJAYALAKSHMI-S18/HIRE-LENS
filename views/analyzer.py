import streamlit as st
import plotly.graph_objects as go
import time
from utils.resume_analyzer import analyze_resume_against_job
from utils.report_generator import generate_html_report, generate_txt_report
from utils.database import save_analysis
from utils.theme import get_plotly_colors, apply_theme

def render():
    st.markdown("<h2 style='text-transform: uppercase;'>🔍 AI RESUME & ATS MATCH ANALYZER</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; text-transform: uppercase;'>UPLOAD YOUR PDF RESUME AND PASTE THE TARGET JOB DESCRIPTION TO RUN RECRUITER-GRADE ATS EVALUATION.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>STEP 1 — UPLOAD RESUME (PDF)</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("CHOOSE PDF RESUME FILE", type=["pdf"], key="analyzer_pdf")
        
        if uploaded_file:
            st.success(f"FILE UPLOADED: **{uploaded_file.name.upper()}** ({round(uploaded_file.size / 1024, 1)} KB)")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>STEP 2 — TARGET JOB DESCRIPTION</h3>", unsafe_allow_html=True)
        job_title = st.text_input("JOB TITLE (OPTIONAL)", placeholder="e.g. Senior Machine Learning Engineer", key="analyzer_job_title")
        job_description = st.text_area("JOB DESCRIPTION REQUIREMENTS", height=150, placeholder="PASTE THE COMPLETE JOB DESCRIPTION TEXT HERE...", key="analyzer_job_desc")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔍 ANALYZE WITH HIRELENS", key="btn_run_analysis"):
        if not uploaded_file:
            st.error("PLEASE UPLOAD A PDF RESUME FILE FIRST.")
            return
        if not job_description.strip():
            st.error("PLEASE PASTE A JOB DESCRIPTION TO COMPARE AGAINST.")
            return

        pdf_bytes = uploaded_file.read()
        
        # Step-by-step progress animation
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        steps = [
            ("READING RESUME PDF TEXT...", 15),
            ("EXTRACTING TECHNICAL & SOFT SKILLS...", 35),
            ("ANALYZING JOB REQUIREMENTS...", 55),
            ("RUNNING SEMANTIC AI MATCHING ENGINE...", 75),
            ("CALCULATING WEIGHTED ATS SCORE...", 90),
            ("GENERATING PERSONALIZED RECOMMENDATIONS...", 100)
        ]
        
        for msg, val in steps:
            progress_text.markdown(f"**🤖 {msg}**")
            progress_bar.progress(val)
            time.sleep(0.12)

        results = analyze_resume_against_job(
            pdf_bytes=pdf_bytes,
            job_description=job_description,
            job_title=job_title
        )

        progress_text.empty()
        progress_bar.empty()

        if not results["success"]:
            st.error(results["error"])
            return

        # Store results in session state for rendering
        st.session_state["last_analysis"] = results
        st.session_state["last_resume_name"] = uploaded_file.name

        # Save to DB if logged in
        if st.session_state.get("user"):
            user_id = st.session_state.user["id"]
            save_analysis(user_id, uploaded_file.name, job_title, results)
            st.toast("ANALYSIS SAVED TO YOUR HISTORY!", icon="💾")

    # Render Results if available
    if "last_analysis" in st.session_state:
        res = st.session_state["last_analysis"]
        resume_name = st.session_state.get("last_resume_name", "Resume.pdf")
        
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-transform: uppercase;'>ANALYSIS RESULTS FOR: <span style='color: #4F8CFF;'>{res['job_title'].upper()}</span></h2>", unsafe_allow_html=True)
        
        # Gauge & Score Summary Row
        sc1, sc2 = st.columns([1, 1])

        with sc1:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; text-transform: uppercase;'>OVERALL ATS SCORE</h3>", unsafe_allow_html=True)
            
            dark_mode = st.session_state.get("dark_mode", True)
            colors = get_plotly_colors(dark_mode)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=res["ats_score"],
                number={'suffix': "%", 'font': {'color': colors['text'], 'size': 50}},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': colors['text']},
                    'bar': {'color': res['interpretation']['color']},
                    'bgcolor': colors['bg'],
                    'bordercolor': colors['grid'],
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.15)'},
                        {'range': [40, 60], 'color': 'rgba(245, 158, 11, 0.15)'},
                        {'range': [60, 80], 'color': 'rgba(79, 140, 255, 0.15)'},
                        {'range': [80, 100], 'color': 'rgba(34, 197, 94, 0.15)'}
                    ]
                }
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=240,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div style='text-align: center; margin-top: -10px;'>
                <div style='display: inline-block; background: {res["interpretation"]["color"]}22; color: {res["interpretation"]["color"]}; border: 1px solid {res["interpretation"]["color"]}44; padding: 6px 16px; border-radius: 20px; font-weight: 700; text-transform: uppercase;'>
                    {res["interpretation"]["badge"]} — {res["interpretation"]["level"]}
                </div>
                <p style='color: #94A3B8; font-size: 0.95rem; margin-top: 10px;'>{res["interpretation"]["summary"]}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with sc2:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-transform: uppercase;'>SCORE BREAKDOWN</h3>", unsafe_allow_html=True)
            
            st.progress(int(res["skill_score"]))
            st.markdown(f"**SKILLS MATCH:** {res['skill_score']}%")
            
            st.progress(int(res["semantic_score"]))
            st.markdown(f"**SEMANTIC AI SIMILARITY:** {res['semantic_score']}%")

            st.progress(int(res["keyword_score"]))
            st.markdown(f"**KEYWORD RELEVANCE:** {res['keyword_score']}%")

            st.progress(int(res["experience_score"]))
            st.markdown(f"**EXPERIENCE MATCH:** {res['experience_score']}% ({res['resume_experience_years']} YRS DETECTED)")

            st.progress(int(res["education_score"]))
            st.markdown(f"**EDUCATION MATCH:** {res['education_score']}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔍 WHY THIS SCORE? (EXPLAINABILITY)", key="btn_why_this_score"):
                st.session_state.current_page = "explainability"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # Matched / Missing / Additional Skills Section
        st.markdown("<br>", unsafe_allow_html=True)
        sk1, sk2, sk3 = st.columns(3)

        with sk1:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-transform: uppercase;'>✅ MATCHED SKILLS ({len(res['matched_skills'])})</h3>", unsafe_allow_html=True)
            if res['matched_skills']:
                html_badges = "".join([f"<span class='skill-badge-matched'>{s.upper()}</span>" for s in res['matched_skills']])
                st.markdown(html_badges, unsafe_allow_html=True)
            else:
                st.info("NO EXACT MATCHING TECHNICAL SKILLS FOUND.")
            st.markdown("</div>", unsafe_allow_html=True)

        with sk2:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-transform: uppercase;'>❌ MISSING SKILLS ({len(res['missing_skills'])})</h3>", unsafe_allow_html=True)
            if res['missing_skills']:
                html_badges = "".join([f"<span class='skill-badge-missing'>{s.upper()}</span>" for s in res['missing_skills']])
                st.markdown(html_badges, unsafe_allow_html=True)
            else:
                st.success("NO REQUIRED SKILLS MISSING!")
            st.markdown("</div>", unsafe_allow_html=True)

        with sk3:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-transform: uppercase;'>➕ ADDITIONAL SKILLS ({len(res['additional_skills'])})</h3>", unsafe_allow_html=True)
            if res['additional_skills']:
                html_badges = "".join([f"<span class='skill-badge-extra'>{s.upper()}</span>" for s in res['additional_skills']])
                st.markdown(html_badges, unsafe_allow_html=True)
            else:
                st.info("NO ADDITIONAL SKILLS DETECTED.")
            st.markdown("</div>", unsafe_allow_html=True)

        # Skill Gap Categorization
        if res.get("skill_gaps_by_category"):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-transform: uppercase;'>🧩 SKILL GAP ANALYSIS BY DOMAIN</h3>", unsafe_allow_html=True)
            for cat, s_list in res["skill_gaps_by_category"].items():
                st.markdown(f"**{cat.upper()}:** " + ", ".join([f"`{s.upper()}`" for s in s_list]))
            st.markdown("</div>", unsafe_allow_html=True)

        # AI Recommendations
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>💡 AI IMPROVEMENT RECOMMENDATIONS</h3>", unsafe_allow_html=True)
        for rec in res["recommendations"]:
            st.markdown(f"""
            <div class='hirelens-card' style='border-left: 4px solid #4F8CFF;'>
                <h4 style='margin-bottom: 6px; text-transform: uppercase;'>{rec['icon']} {rec['title']}</h4>
                <p style='color: #94A3B8; font-size: 0.95rem; margin-bottom: 0;'>{rec['text']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Download Report Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='hirelens-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>📥 DOWNLOAD ANALYSIS REPORT</h3>", unsafe_allow_html=True)
        
        user_name = st.session_state.user["name"] if st.session_state.get("user") else "Candidate"
        html_report = generate_html_report(res, candidate_name=user_name, resume_filename=resume_name)
        txt_report = generate_txt_report(res, candidate_name=user_name, resume_filename=resume_name)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                label="📄 DOWNLOAD HTML REPORT (PRINT TO PDF)",
                data=html_report,
                file_name=f"HireLens_Report_{user_name.replace(' ', '_')}.html",
                mime="text/html",
                key="btn_dl_html"
            )
        with dl2:
            st.download_button(
                label="📝 DOWNLOAD TXT REPORT",
                data=txt_report,
                file_name=f"HireLens_Report_{user_name.replace(' ', '_')}.txt",
                mime="text/plain",
                key="btn_dl_txt"
            )
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
