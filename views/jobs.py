import streamlit as st
import pandas as pd
import plotly.express as px
from utils.resume_analyzer import analyze_resume_against_job
from utils.theme import get_plotly_colors

def render():
    st.markdown("<h2 style='text-transform: uppercase;'>💼 MULTIPLE JOB MATCH COMPARISON</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; text-transform: uppercase;'>UPLOAD YOUR RESUME ONCE AND ANALYZE IT AGAINST MULTIPLE TARGET JOB POSTINGS TO DISCOVER: <strong>“WHICH JOB FITS ME BEST?”</strong></p>", unsafe_allow_html=True)

    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("UPLOAD RESUME PDF", type=["pdf"], key="jobs_pdf")
    st.markdown("</div>", unsafe_allow_html=True)

    num_jobs = st.slider("NUMBER OF TARGET JOBS TO COMPARE", min_value=2, max_value=4, value=2, key="slider_num_jobs")

    job_inputs = []
    cols = st.columns(num_jobs)
    
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<div class='hirelens-card'>", unsafe_allow_html=True)
            j_title = st.text_input(f"JOB #{i+1} TITLE", value=f"POSITION #{i+1}", key=f"job_title_{i}")
            j_desc = st.text_area(f"JOB #{i+1} REQUIREMENTS", height=160, placeholder="Paste job description...", key=f"job_desc_{i}")
            job_inputs.append({"title": j_title, "desc": j_desc})
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 COMPARE JOB FITS", key="btn_compare_jobs"):
        if not uploaded_file:
            st.error("PLEASE UPLOAD A PDF RESUME FILE.")
            return
            
        pdf_bytes = uploaded_file.read()
        
        valid_jobs = [j for j in job_inputs if j["desc"].strip()]
        if len(valid_jobs) < 2:
            st.error("PLEASE PROVIDE AT LEAST 2 JOB DESCRIPTIONS TO COMPARE.")
            return

        comparison_results = []
        with st.spinner("ANALYZING CANDIDATE COMPATIBILITY ACROSS JOB LISTINGS..."):
            for j in valid_jobs:
                res = analyze_resume_against_job(pdf_bytes, j["desc"], j["title"])
                if res["success"]:
                    comparison_results.append({
                        "title": j["title"].upper(),
                        "ats_score": res["ats_score"],
                        "skill_score": res["skill_score"],
                        "semantic_score": res["semantic_score"],
                        "keyword_score": res["keyword_score"],
                        "matched_count": len(res["matched_skills"]),
                        "missing_count": len(res["missing_skills"]),
                        "badge": res["interpretation"]["badge"],
                        "color": res["interpretation"]["color"]
                    })

        if not comparison_results:
            st.error("COULD NOT PARSE RESUME OR JOB DESCRIPTIONS.")
            return

        df_comp = pd.DataFrame(comparison_results).sort_values(by="ats_score", ascending=False)
        
        best_fit = df_comp.iloc[0]

        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='hirelens-card' style='border: 2px solid #22C55E; background: rgba(34, 197, 94, 0.08); text-align: center;'>
            <h3 style='color: #22C55E; margin-bottom: 4px; text-transform: uppercase;'>🏆 HIGHEST MATCH RECOMMENDATION</h3>
            <h2 style='font-size: 2.2rem; margin-bottom: 8px; text-transform: uppercase;'>{best_fit['title']}</h2>
            <div style='font-size: 1.8rem; font-weight: 800; color: #22C55E;'>{best_fit['ats_score']}% ATS FIT</div>
            <p style='color: #94A3B8; margin-top: 8px; text-transform: uppercase;'>YOUR SKILLS AND EXPERIENCE ALIGN MOST CLOSELY WITH THIS POSITION.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>JOB FIT LEADERBOARD COMPARISON</h3>", unsafe_allow_html=True)
        
        dark_mode = st.session_state.get("dark_mode", True)
        colors = get_plotly_colors(dark_mode)

        fig_comp = px.bar(
            df_comp,
            x="title",
            y=["ats_score", "skill_score", "semantic_score"],
            barmode="group",
            labels={"value": "SCORE (%)", "title": "TARGET ROLE", "variable": "METRIC"},
            color_discrete_sequence=[colors['blue'], colors['purple'], colors['cyan']]
        )
        fig_comp.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text']),
            height=320
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
