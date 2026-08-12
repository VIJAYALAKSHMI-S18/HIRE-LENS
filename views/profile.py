import streamlit as st
from utils.database import get_user_analyses, update_user_profile

def render():
    if not st.session_state.get("user"):
        st.warning("PLEASE LOG IN TO VIEW YOUR PROFILE.")
        return

    user = st.session_state.user
    history = get_user_analyses(user["id"])

    st.markdown("<h2 style='text-transform: uppercase;'>👤 CANDIDATE PROFILE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; text-transform: uppercase;'>MANAGE YOUR ACCOUNT CREDENTIALS AND VIEW LIFETIME CANDIDATE STATISTICS.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>PROFILE SUMMARY</h3>", unsafe_allow_html=True)
        st.markdown(f"**FULL NAME:** {user['name'].upper()}")
        st.markdown(f"**EMAIL ADDRESS:** {user['email'].upper()}")
        st.markdown(f"**TOTAL RESUME ANALYSES:** {len(history)}")
        
        if history:
            avg_s = round(sum(h['ats_score'] for h in history) / len(history), 1)
            max_s = round(max(h['ats_score'] for h in history), 1)
            st.markdown(f"**AVERAGE ATS COMPATIBILITY:** {avg_s}%")
            st.markdown(f"**HIGHEST RECORDED ATS FIT:** {max_s}%")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>UPDATE PROFILE & SECURITY</h3>", unsafe_allow_html=True)
        
        new_name = st.text_input("DISPLAY NAME", value=user["name"].upper(), key="prof_name")
        new_pwd = st.text_input("NEW PASSWORD (OPTIONAL)", type="password", key="prof_pwd")
        new_pwd_confirm = st.text_input("CONFIRM NEW PASSWORD", type="password", key="prof_pwd_confirm")

        if st.button("SAVE PROFILE CHANGES", key="btn_save_prof"):
            if not new_name.strip():
                st.error("NAME CANNOT BE EMPTY.")
            elif new_pwd and new_pwd != new_pwd_confirm:
                st.error("PASSWORDS DO NOT MATCH.")
            elif new_pwd and len(new_pwd) < 6:
                st.error("PASSWORD MUST BE AT LEAST 6 CHARACTERS.")
            else:
                update_user_profile(user["id"], new_name, new_pwd if new_pwd else None)
                st.session_state.user["name"] = new_name.strip()
                st.success("PROFILE UPDATED SUCCESSFULLY!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
