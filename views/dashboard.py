import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.database import get_user_analyses
from utils.theme import get_plotly_colors

def render():
    if not st.session_state.get("user"):
        st.warning("PLEASE LOG IN TO VIEW YOUR PERSONALIZED ANALYTICS DASHBOARD.")
        return

    user = st.session_state.user
    st.markdown("<h2 style='text-transform: uppercase;'>📊 RECRUITER ANALYTICS & CAREER DASHBOARD</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94A3B8; text-transform: uppercase;'>WELCOME BACK, <strong>{user['name'].upper()}</strong>! TRACK YOUR ATS SCORES, SKILL MATCHES, AND RESUME PERFORMANCE HISTORY.</p>", unsafe_allow_html=True)

    history = get_user_analyses(user["id"])

    if not history:
        st.info("NO ANALYSIS HISTORY RECORDED YET. HEAD OVER TO THE RESUME ANALYZER TO RUN YOUR FIRST EVALUATION!")
        if st.button("🚀 ANALYZE FIRST RESUME", key="dash_btn_first"):
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
        st.metric(label="TOTAL ANALYSES", value=total_analyses)
    with c2:
        st.metric(label="AVERAGE ATS SCORE", value=f"{avg_ats}%")
    with c3:
        st.metric(label="HIGHEST ATS FIT", value=f"{max_ats}%")
    with c4:
        st.metric(label="SKILLS MATCHED", value=total_matched_skills)

    st.markdown("<br>", unsafe_allow_html=True)

    dark_mode = st.session_state.get("dark_mode", True)
    colors = get_plotly_colors(dark_mode)

    # Charts Row
    ch1, ch2 = st.columns([1, 1])

    with ch1:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>ATS SCORE HISTORY</h3>", unsafe_allow_html=True)
        
        fig_hist = px.bar(
            df,
            x="created_at",
            y="ats_score",
            hover_data=["job_title", "resume_name"],
            labels={"ats_score": "ATS SCORE (%)", "created_at": "DATE"},
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
        st.markdown("<h3 style='text-transform: uppercase;'>LATEST SCORE BREAKDOWN</h3>", unsafe_allow_html=True)
        latest = df.iloc[0]
        
        metrics = ["SKILLS MATCH", "SEMANTIC MATCH", "KEYWORDS", "EXPERIENCE", "EDUCATION"]
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
    st.markdown("<h3 style='text-transform: uppercase;'>RECENT TARGET JOB FITS</h3>", unsafe_allow_html=True)
    
    display_df = df[["job_title", "resume_name", "ats_score", "skill_score", "semantic_score", "created_at"]].copy()
    display_df.columns = ["JOB TITLE", "RESUME FILE", "ATS SCORE (%)", "SKILL SCORE (%)", "SEMANTIC MATCH (%)", "ANALYSIS DATE"]
    
    st.dataframe(display_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
