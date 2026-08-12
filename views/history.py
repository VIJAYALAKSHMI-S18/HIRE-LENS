import streamlit as st
from utils.database import get_user_analyses, delete_analysis
from utils.report_generator import generate_html_report, generate_txt_report

def render():
    if not st.session_state.get("user"):
        st.warning("PLEASE LOG IN TO VIEW YOUR SAVED ANALYSIS HISTORY.")
        return

    user = st.session_state.user
    st.markdown("<h2 style='text-transform: uppercase;'>🕘 SAVED ANALYSIS HISTORY</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94A3B8; text-transform: uppercase;'>REVIEW, RE-EXAMINE, AND DOWNLOAD PAST ATS REPORTS FOR <strong>{user['name'].upper()}</strong>.</p>", unsafe_allow_html=True)

    history = get_user_analyses(user["id"])

    if not history:
        st.info("NO SAVED ANALYSIS RECORDS FOUND.")
        return

    for item in history:
        with st.expander(f"📄 {item['job_title'].upper()} — {item['ats_score']}% ATS SCORE ({item['created_at']})"):
            st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**RESUME:** {item['resume_name'].upper()}")
                st.write(f"**DATE:** {item['created_at']}")
            with c2:
                st.write(f"**ATS SCORE:** {item['ats_score']}%")
                st.write(f"**SKILL SCORE:** {item['skill_score']}%")
            with c3:
                st.write(f"**SEMANTIC MATCH:** {item['semantic_score']}%")
                st.write(f"**KEYWORDS MATCH:** {item['keyword_score']}%")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### MATCHED SKILLS:")
            st.write(", ".join([s.upper() for s in item['matched_skills']]) or "NONE")

            st.markdown("#### MISSING SKILLS:")
            st.write(", ".join([s.upper() for s in item['missing_skills']]) or "NONE")

            st.markdown("<br>", unsafe_allow_html=True)
            
            html_rep = generate_html_report(item, candidate_name=user['name'], resume_filename=item['resume_name'])
            txt_rep = generate_txt_report(item, candidate_name=user['name'], resume_filename=item['resume_name'])

            d1, d2, d3 = st.columns([2, 2, 1])
            with d1:
                st.download_button(
                    label="📄 DOWNLOAD HTML REPORT",
                    data=html_rep,
                    file_name=f"HireLens_Report_{item['id']}.html",
                    mime="text/html",
                    key=f"hist_dl_html_{item['id']}"
                )
            with d2:
                st.download_button(
                    label="📝 DOWNLOAD TXT REPORT",
                    data=txt_rep,
                    file_name=f"HireLens_Report_{item['id']}.txt",
                    mime="text/plain",
                    key=f"hist_dl_txt_{item['id']}"
                )
            with d3:
                if st.button("🗑️ DELETE", key=f"hist_del_{item['id']}"):
                    delete_analysis(item['id'], user['id'])
                    st.toast("RECORD DELETED.", icon="🗑️")
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
