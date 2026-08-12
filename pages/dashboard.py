import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.database import get_user_analyses
from utils.theme import get_plotly_colors

def render():
    if not st.session_state.get("user"):
        st.warning("Please log in to view your personalized analytics dashboard.")
        return

    user = st.session_state.user
    st.markdown(f"<h2>📊 Recruiter Analytics & Career Dashboard</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94A3B8;'>Welcome back, <strong>{user['name']}</strong>! Track your ATS scores, skill matches, and resume performance history.</p>", unsafe_allow_html=True)

    history = get_user_analyses(user["id"])

    if not history:
        st.info("No analysis history recorded yet. Head over to the **Resume Analyzer** to run your first evaluation!")
        if st.button("🚀 Analyze First Resume", key="dash_btn_first"):
            st.session_state.current_page = "analyzer"
            st.rerun()
        return

    df = pd.DataFrame(history)

    # Summary Stat Cards
    total_analyses = len(df)
    avg_ats = round(df["ats_score"].mean(), 1)
    max_ats = round(df["ats_score"].max(), 1)
    
    total_matched_skills = sum([len(m) for m in df["matched_skills"]])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Total Analyses", value=total_analyses)
    with c2:
        st.metric(label="Average ATS Score", value=f"{avg_ats}%")
    with c3:
        st.metric(label="Highest ATS Fit", value=f"{max_ats}%")
    with c4:
        st.metric(label="Skills Matched", value=total_matched_skills)

    st.markdown("<br>", unsafe_allow_html=True)

    dark_mode = st.session_state.get("dark_mode", True)
    colors = get_plotly_colors(dark_mode)

    # Charts Row
    ch1, ch2 = st.columns([1, 1])

    with ch1:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("### ATS Score History")
        
        fig_hist = px.bar(
            df,
            x="created_at",
            y="ats_score",
            hover_data=["job_title", "resume_name"],
            labels={"ats_score": "ATS Score (%)", "created_at": "Date"},
            color="ats_score",
            color_continuous_scale=["#EF4444", "#F59E0B", "#4F8CFF", "#22C55E"]
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text']),
            height=300,
            margin=dict(l=10, r=10, t=20, b=20)
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with ch2:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("### Latest Score Breakdown")
        latest = df.iloc[0]
        
        metrics = ["Skills Match", "Semantic Match", "Keywords", "Experience", "Education"]
        scores = [
            latest["skill_score"],
            latest["semantic_score"],
            latest["keyword_score"],
            latest["experience_score"],
            latest["education_score"]
        ]
        
        fig_donut = px.pie(
            names=metrics,
            values=scores,
            hole=0.5,
            color_discrete_sequence=[colors['blue'], colors['purple'], colors['cyan'], colors['green'], colors['yellow']]
        )
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text']),
            height=300,
            margin=dict(l=10, r=10, t=20, b=20)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Recent Records Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("### Recent Target Job Fits")
    
    display_df = df[["job_title", "resume_name", "ats_score", "skill_score", "semantic_score", "created_at"]].copy()
    display_df.columns = ["Job Title", "Resume File", "ATS Score (%)", "Skill Score (%)", "Semantic Match (%)", "Analysis Date"]
    
    st.dataframe(display_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
