import streamlit as st
import plotly.graph_objects as go
import time
from utils.resume_analyzer import analyze_resume_against_job
from utils.report_generator import generate_html_report, generate_txt_report
from utils.database import save_analysis
from utils.theme import get_plotly_colors

def render():
    st.markdown("<h2>🔍 AI Resume & ATS Match Analyzer</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>Upload your PDF resume and paste the target job description to run recruiter-grade ATS evaluation.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("### Step 1 — Upload Resume (PDF)")
        uploaded_file = st.file_uploader("Choose PDF Resume File", type=["pdf"], key="analyzer_pdf")
        
        if uploaded_file:
            st.success(f"File uploaded: **{uploaded_file.name}** ({round(uploaded_file.size / 1024, 1)} KB)")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("### Step 2 — Target Job Description")
        job_title = st.text_input("Job Title (Optional)", placeholder="e.g. Senior Machine Learning Engineer", key="analyzer_job_title")
        job_description = st.text_area("Job Description Requirements", height=150, placeholder="Paste the complete job description text here...", key="analyzer_job_desc")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔍 Analyze with HireLens", key="btn_run_analysis"):
        if not uploaded_file:
            st.error("Please upload a PDF resume file first.")
            return
        if not job_description.strip():
            st.error("Please paste a job description to compare against.")
            return

        pdf_bytes = uploaded_file.read()
        
        # Step-by-step progress animation
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        steps = [
            ("Reading resume PDF text...", 15),
            ("Extracting technical & soft skills...", 35),
            ("Analyzing job requirements...", 55),
            ("Running semantic AI matching engine...", 75),
            ("Calculating weighted ATS score...", 90),
            ("Generating personalized recommendations...", 100)
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
            st.toast("Analysis saved to your history!", icon="💾")

    # Render Results if available
    if "last_analysis" in st.session_state:
        res = st.session_state["last_analysis"]
        resume_name = st.session_state.get("last_resume_name", "Resume.pdf")
        
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown(f"## Analysis Results for: <span style='color: #4F8CFF;'>{res['job_title']}</span>", unsafe_allow_html=True)
        
        # Gauge & Score Summary Row
        sc1, sc2 = st.columns([1, 1])

        with sc1:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>Overall ATS Score</h3>", unsafe_allow_html=True)
            
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
                <div style='display: inline-block; background: {res["interpretation"]["color"]}22; color: {res["interpretation"]["color"]}; border: 1px solid {res["interpretation"]["color"]}44; padding: 6px 16px; border-radius: 20px; font-weight: 700;'>
                    {res["interpretation"]["badge"]} — {res["interpretation"]["level"]}
                </div>
                <p style='color: #94A3B8; font-size: 0.95rem; margin-top: 10px;'>{res["interpretation"]["summary"]}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with sc2:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown("### Score Breakdown")
            
            st.progress(int(res["skill_score"]))
            st.markdown(f"**Skills Match:** {res['skill_score']}%")
            
            st.progress(int(res["semantic_score"]))
            st.markdown(f"**Semantic AI Similarity:** {res['semantic_score']}%")

            st.progress(int(res["keyword_score"]))
            st.markdown(f"**Keyword Relevance:** {res['keyword_score']}%")

            st.progress(int(res["experience_score"]))
            st.markdown(f"**Experience Match:** {res['experience_score']}% ({res['resume_experience_years']} yrs detected)")

            st.progress(int(res["education_score"]))
            st.markdown(f"**Education Match:** {res['education_score']}%")
            st.markdown("</div>", unsafe_allow_html=True)

        # Matched / Missing / Additional Skills Section
        st.markdown("<br>", unsafe_allow_html=True)
        sk1, sk2, sk3 = st.columns(3)

        with sk1:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown(f"### ✅ Matched Skills ({len(res['matched_skills'])})")
            if res['matched_skills']:
                html_badges = "".join([f"<span class='skill-badge-matched'>{s}</span>" for s in res['matched_skills']])
                st.markdown(html_badges, unsafe_allow_html=True)
            else:
                st.info("No exact matching technical skills found.")
            st.markdown("</div>", unsafe_allow_html=True)

        with sk2:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown(f"### ❌ Missing Skills ({len(res['missing_skills'])})")
            if res['missing_skills']:
                html_badges = "".join([f"<span class='skill-badge-missing'>{s}</span>" for s in res['missing_skills']])
                st.markdown(html_badges, unsafe_allow_html=True)
            else:
                st.success("No required skills missing!")
            st.markdown("</div>", unsafe_allow_html=True)

        with sk3:
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown(f"### ➕ Additional Skills ({len(res['additional_skills'])})")
            if res['additional_skills']:
                html_badges = "".join([f"<span class='skill-badge-extra'>{s}</span>" for s in res['additional_skills']])
                st.markdown(html_badges, unsafe_allow_html=True)
            else:
                st.info("No additional skills detected.")
            st.markdown("</div>", unsafe_allow_html=True)

        # Skill Gap Categorization
        if res.get("skill_gaps_by_category"):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            st.markdown("### 🧩 Skill Gap Analysis by Domain")
            for cat, s_list in res["skill_gaps_by_category"].items():
                st.markdown(f"**{cat}:** " + ", ".join([f"`{s}`" for s in s_list]))
            st.markdown("</div>", unsafe_allow_html=True)

        # AI Recommendations
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💡 AI Improvement Recommendations")
        for rec in res["recommendations"]:
            st.markdown(f"""
            <div class='hirelens-card' style='border-left: 4px solid #4F8CFF;'>
                <h4 style='margin-bottom: 6px;'>{rec['icon']} {rec['title']}</h4>
                <p style='color: #94A3B8; font-size: 0.95rem; margin-bottom: 0;'>{rec['text']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Download Report Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='hirelens-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("### 📥 Download Analysis Report")
        
        user_name = st.session_state.user["name"] if st.session_state.get("user") else "Candidate"
        html_report = generate_html_report(res, candidate_name=user_name, resume_filename=resume_name)
        txt_report = generate_txt_report(res, candidate_name=user_name, resume_filename=resume_name)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                label="📄 Download HTML Report (Print to PDF)",
                data=html_report,
                file_name=f"HireLens_Report_{user_name.replace(' ', '_')}.html",
                mime="text/html",
                key="btn_dl_html"
            )
        with dl2:
            st.download_button(
                label="📝 Download TXT Report",
                data=txt_report,
                file_name=f"HireLens_Report_{user_name.replace(' ', '_')}.txt",
                mime="text/plain",
                key="btn_dl_txt"
            )
        st.markdown("</div>", unsafe_allow_html=True)
