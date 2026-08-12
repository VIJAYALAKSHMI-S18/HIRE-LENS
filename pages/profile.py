import streamlit as st
from utils.database import get_user_analyses, update_user_profile

def render():
    if not st.session_state.get("user"):
        st.warning("Please log in to view your profile.")
        return

    user = st.session_state.user
    history = get_user_analyses(user["id"])

    st.markdown("<h2>👤 Candidate Profile</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>Manage your account credentials and view lifetime candidate statistics.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("### Profile Summary")
        st.markdown(f"**Full Name:** {user['name']}")
        st.markdown(f"**Email Address:** {user['email']}")
        st.markdown(f"**Total Resume Analyses:** {len(history)}")
        
        if history:
            avg_s = round(sum(h['ats_score'] for h in history) / len(history), 1)
            max_s = round(max(h['ats_score'] for h in history), 1)
            st.markdown(f"**Average ATS Compatibility:** {avg_s}%")
            st.markdown(f"**Highest Recorded ATS Fit:** {max_s}%")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("### Update Profile & Security")
        
        new_name = st.text_input("Display Name", value=user["name"], key="prof_name")
        new_pwd = st.text_input("New Password (Optional)", type="password", key="prof_pwd")
        new_pwd_confirm = st.text_input("Confirm New Password", type="password", key="prof_pwd_confirm")

        if st.button("Save Profile Changes", key="btn_save_prof"):
            if not new_name.strip():
                st.error("Name cannot be empty.")
            elif new_pwd and new_pwd != new_pwd_confirm:
                st.error("Passwords do not match.")
            elif new_pwd and len(new_pwd) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                update_user_profile(user["id"], new_name, new_pwd if new_pwd else None)
                st.session_state.user["name"] = new_name.strip()
                st.success("Profile updated successfully!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
