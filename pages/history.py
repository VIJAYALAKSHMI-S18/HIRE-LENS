import streamlit as st
from utils.database import get_user_analyses, delete_analysis
from utils.report_generator import generate_html_report, generate_txt_report

def render():
    if not st.session_state.get("user"):
        st.warning("Please log in to view your saved analysis history.")
        return

    user = st.session_state.user
    st.markdown("<h2>🕘 Saved Analysis History</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94A3B8;'>Review, re-examine, and download past ATS reports for <strong>{user['name']}</strong>.</p>", unsafe_allow_html=True)

    history = get_user_analyses(user["id"])

    if not history:
        st.info("No saved analysis records found.")
        return

    for item in history:
        with st.expander(f"📄 {item['job_title']} — {item['ats_score']}% ATS Score ({item['created_at']})"):
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**Resume:** {item['resume_name']}")
                st.write(f"**Date:** {item['created_at']}")
            with c2:
                st.write(f"**ATS Score:** {item['ats_score']}%")
                st.write(f"**Skill Score:** {item['skill_score']}%")
            with c3:
                st.write(f"**Semantic Match:** {item['semantic_score']}%")
                st.write(f"**Keywords Match:** {item['keyword_score']}%")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Matched Skills:")
            st.write(", ".join(item['matched_skills']) or "None")

            st.markdown("#### Missing Skills:")
            st.write(", ".join(item['missing_skills']) or "None")

            st.markdown("<br>", unsafe_allow_html=True)
            
            html_rep = generate_html_report(item, candidate_name=user['name'], resume_filename=item['resume_name'])
            txt_rep = generate_txt_report(item, candidate_name=user['name'], resume_filename=item['resume_name'])

            d1, d2, d3 = st.columns([2, 2, 1])
            with d1:
                st.download_button(
                    label="📄 Download HTML Report",
                    data=html_rep,
                    file_name=f"HireLens_Report_{item['id']}.html",
                    mime="text/html",
                    key=f"hist_dl_html_{item['id']}"
                )
            with d2:
                st.download_button(
                    label="📝 Download TXT Report",
                    data=txt_rep,
                    file_name=f"HireLens_Report_{item['id']}.txt",
                    mime="text/plain",
                    key=f"hist_dl_txt_{item['id']}"
                )
            with d3:
                if st.button("🗑️ Delete", key=f"hist_del_{item['id']}"):
                    delete_analysis(item['id'], user['id'])
                    st.toast("Record deleted.", icon="🗑️")
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)
