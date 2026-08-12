import streamlit as st
from utils.database import authenticate_user, register_user

def init_auth_session():
    """Initializes Streamlit authentication session state."""
    if "user" not in st.session_state:
        st.session_state.user = None
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True
    if "reduced_motion" not in st.session_state:
        st.session_state.reduced_motion = False

def is_logged_in() -> bool:
    return st.session_state.get("user") is not None

def logout():
    st.session_state.user = None
    st.rerun()

def render_login_signup():
    """Renders sleek Login / Sign Up UI component in Streamlit."""
    st.markdown("<h2 style='text-align: center; margin-bottom: 24px;'>Welcome to HireLens 🎯</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Account Login", "🚀 Register Account"])
    
    with tab1:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_pwd")
        
        if st.button("Sign In to HireLens", key="btn_login"):
            if not email or not password:
                st.error("Please fill in all credentials.")
            else:
                success, user_data = authenticate_user(email, password)
                if success:
                    st.session_state.user = user_data
                    st.success(f"Welcome back, {user_data['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab2:
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email Address", key="reg_email")
        reg_pwd = st.text_input("Password", type="password", key="reg_pwd")
        reg_pwd_confirm = st.text_input("Confirm Password", type="password", key="reg_pwd_confirm")
        
        if st.button("Create My Account", key="btn_reg"):
            if not name or not reg_email or not reg_pwd or not reg_pwd_confirm:
                st.error("Please complete all registration fields.")
            elif reg_pwd != reg_pwd_confirm:
                st.error("Passwords do not match.")
            elif len(reg_pwd) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                success, msg, user_id = register_user(name, reg_email, reg_pwd)
                if success:
                    st.success("Account created successfully! Logging you in...")
                    st.session_state.user = {"id": user_id, "name": name, "email": reg_email}
                    st.rerun()
                else:
                    st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)
