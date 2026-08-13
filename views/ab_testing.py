import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.resume_analyzer import analyze_resume_against_job
from utils.database import save_ab_test, get_user_ab_tests
from utils.theme import get_plotly_colors

def render():
    st.markdown("<h2 style='text-transform: uppercase;'>📊 RESUME A/B TESTING & COMPARISON</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; text-transform: uppercase;'>EVALUATE TWO VERSIONS OF YOUR RESUME AGAINST THE EXACT SAME JOB DESCRIPTION TO MEASURE WHICH ONE SCORES HIGHER WITH ATS FILTERS.</p>", unsafe_allow_html=True)

    # Job Description Input
    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-transform: uppercase;'>STEP 1 — TARGET JOB DESCRIPTION</h3>", unsafe_allow_html=True)
    job_title = st.text_input("TARGET JOB TITLE", placeholder="e.g. Machine Learning Engineer", key="ab_job_title")
    job_desc = st.text_area("JOB REQUIREMENTS", height=130, placeholder="Paste target job description text here...", key="ab_job_desc")
    st.markdown("</div>", unsafe_allow_html=True)

    # Resumes Input
    c_a, c_b = st.columns(2)

    with c_a:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>RESUME VERSION A</h3>", unsafe_allow_html=True)
        label_a = st.text_input("VERSION A LABEL", value="Original Resume", key="ab_label_a")
        file_a = st.file_uploader("UPLOAD RESUME A (PDF)", type=["pdf"], key="ab_file_a")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_b:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>RESUME VERSION B</h3>", unsafe_allow_html=True)
        label_b = st.text_input("VERSION B LABEL", value="Updated Resume", key="ab_label_b")
        file_b = st.file_uploader("UPLOAD RESUME B (PDF)", type=["pdf"], key="ab_file_b")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ COMPARE RESUMES", key="btn_run_ab_test"):
        if not job_desc.strip():
            st.error("PLEASE PROVIDE A TARGET JOB DESCRIPTION.")
            return
        if not file_a:
            st.error("PLEASE UPLOAD RESUME VERSION A.")
            return
        if not file_b:
            st.error("PLEASE UPLOAD RESUME VERSION B.")
            return

        pdf_bytes_a = file_a.read()
        pdf_bytes_b = file_b.read()

        with st.spinner(f"RUNNING ATS EVALUATION FOR BOTH '{label_a.upper()}' AND '{label_b.upper()}'..."):
            res_a = analyze_resume_against_job(pdf_bytes_a, job_desc, job_title)
            res_b = analyze_resume_against_job(pdf_bytes_b, job_desc, job_title)

        if not res_a["success"]:
            st.error(f"Error parsing Resume A: {res_a['error']}")
            return
        if not res_b["success"]:
            st.error(f"Error parsing Resume B: {res_b['error']}")
            return

        st.session_state["ab_test_results"] = {
            "res_a": res_a,
            "res_b": res_b,
            "label_a": label_a,
            "label_b": label_b,
            "file_a_name": file_a.name,
            "file_b_name": file_b.name,
            "job_title": job_title
        }

        # Save to DB if logged in
        if st.session_state.get("user"):
            user_id = st.session_state.user["id"]
            diff = res_b["ats_score"] - res_a["ats_score"]
            winner = label_b if diff >= 0 else label_a
            save_ab_test(
                user_id=user_id,
                resume_a_name=file_a.name,
                resume_b_name=file_b.name,
                job_title=job_title,
                score_a=res_a["ats_score"],
                score_b=res_b["ats_score"],
                winner_label=winner
            )
            st.toast("A/B TEST SAVED TO YOUR HISTORY!", icon="💾")

    # Render A/B Test Results if available
    if "ab_test_results" in st.session_state:
        ab = st.session_state["ab_test_results"]
        ra = ab["res_a"]
        rb = ab["res_b"]
        la = ab["label_a"]
        lb = ab["label_b"]

        diff = round(rb["ats_score"] - ra["ats_score"], 1)
        
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        
        # Winner Banner
        if diff > 0:
            st.markdown(f"""
            <div class='hirelens-card' style='border: 2px solid #22C55E; background: rgba(34, 197, 94, 0.08); text-align: center;'>
                <h3 style='color: #22C55E; margin: 0; text-transform: uppercase;'>🏆 {lb.upper()} PERFORMS BETTER</h3>
                <div style='font-size: 2.2rem; font-weight: 800; color: #22C55E; margin: 8px 0;'>+{diff}% ATS SCORE IMPROVEMENT</div>
                <p style='color: #94A3B8; margin: 0;'>{lb} scored <strong>{rb['ats_score']}%</strong> vs {la} <strong>{ra['ats_score']}%</strong> against {ab['job_title'] or 'target role'}.</p>
            </div>
            """, unsafe_allow_html=True)
        elif diff < 0:
            st.markdown(f"""
            <div class='hirelens-card' style='border: 2px solid #4F8CFF; background: rgba(79, 140, 255, 0.08); text-align: center;'>
                <h3 style='color: #4F8CFF; margin: 0; text-transform: uppercase;'>🏆 {la.upper()} PERFORMS BETTER</h3>
                <div style='font-size: 2.2rem; font-weight: 800; color: #4F8CFF; margin: 8px 0;'>+{abs(diff)}% HIGHER ATS SCORE</div>
                <p style='color: #94A3B8; margin: 0;'>{la} scored <strong>{ra['ats_score']}%</strong> vs {lb} <strong>{rb['ats_score']}%</strong>.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='hirelens-card' style='border: 2px solid #38BDF8; text-align: center;'>
                <h3 style='color: #38BDF8; margin: 0; text-transform: uppercase;'>🤝 EQUAL SCORE MATCH ({ra['ats_score']}%)</h3>
                <p style='color: #94A3B8; margin-top: 8px;'>Both versions achieved identical overall ATS compatibility ratings.</p>
            </div>
            """, unsafe_allow_html=True)

        # Comparison Matrix Table
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>📊 SIDE-BY-SIDE METRIC COMPARISON</h3>", unsafe_allow_html=True)

        comp_data = {
            "EVALUATION METRIC": ["Overall ATS Score", "Skill Match", "Semantic AI Match", "Keyword Match", "Experience Match", "Education Match"],
            f"{la.upper()}": [f"{ra['ats_score']}%", f"{ra['skill_score']}%", f"{ra['semantic_score']}%", f"{ra['keyword_score']}%", f"{ra['experience_score']}%", f"{ra['education_score']}%"],
            f"{lb.upper()}": [f"{rb['ats_score']}%", f"{rb['skill_score']}%", f"{rb['semantic_score']}%", f"{rb['keyword_score']}%", f"{rb['experience_score']}%", f"{rb['education_score']}%"],
            "DIFFERENCE": [f"{'+' if diff >= 0 else ''}{diff}%", f"{round(rb['skill_score'] - ra['skill_score'], 1)}%", f"{round(rb['semantic_score'] - ra['semantic_score'], 1)}%", f"{round(rb['keyword_score'] - ra['keyword_score'], 1)}%", f"{round(rb['experience_score'] - ra['experience_score'], 1)}%", f"{round(rb['education_score'] - ra['education_score'], 1)}%"]
        }
        st.table(pd.DataFrame(comp_data))
        st.markdown("</div>", unsafe_allow_html=True)

        # Visual Plotly Chart
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>📈 VISUAL SCORE COMPARISON CHART</h3>", unsafe_allow_html=True)

        dark_mode = st.session_state.get("dark_mode", True)
        colors = get_plotly_colors(dark_mode)

        categories = ["ATS Score", "Skills Match", "Semantic Match", "Keywords", "Experience"]
        scores_a = [ra['ats_score'], ra['skill_score'], ra['semantic_score'], ra['keyword_score'], ra['experience_score']]
        scores_b = [rb['ats_score'], rb['skill_score'], rb['semantic_score'], rb['keyword_score'], rb['experience_score']]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=categories, y=scores_a, name=la.upper(), marker_color=colors['blue']))
        fig.add_trace(go.Bar(x=categories, y=scores_b, name=lb.upper(), marker_color=colors['purple']))

        fig.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text']),
            height=320,
            margin=dict(l=10, r=10, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Skills Gained / Lost Section
        skills_a = set(ra["matched_skills"])
        skills_b = set(rb["matched_skills"])

        gained = sorted(list(skills_b - skills_a))
        lost = sorted(list(skills_a - skills_b))

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>🧩 SKILL MATCH VARIANCE</h3>", unsafe_allow_html=True)

        g_col, l_col = st.columns(2)
        with g_col:
            st.markdown(f"**SKILLS GAINED IN {lb.upper()} ({len(gained)}):**")
            if gained:
                for s in gained:
                    st.markdown(f"<span class='skill-badge-matched'>+ {s.upper()}</span>", unsafe_allow_html=True)
            else:
                st.write("None gained.")

        with l_col:
            st.markdown(f"**SKILLS REMOVED IN {lb.upper()} ({len(lost)}):**")
            if lost:
                for s in lost:
                    st.markdown(f"<span class='skill-badge-missing'>- {s.upper()}</span>", unsafe_allow_html=True)
            else:
                st.write("None lost.")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
